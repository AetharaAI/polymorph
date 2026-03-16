"""
Memory Service - Integrates Redis, MongoDB, Qdrant, PostgreSQL, and BGE services.
"""
import os
import json
import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from backend.config.bootstrap import load_harness_env

load_harness_env()

import redis.asyncio as redis
from motor.motor_asyncio import AsyncIOMotorClient
from qdrant_client import AsyncQdrantClient
import asyncpg
import httpx


class _InMemoryRedis:
    """Minimal async Redis-like store for degraded local mode."""

    def __init__(self):
        self._hashes: dict[str, dict[str, str]] = {}
        self._zsets: dict[str, dict[str, float]] = {}

    async def ping(self) -> bool:
        return True

    async def aclose(self) -> None:
        return None

    async def exists(self, key: str) -> int:
        return 1 if key in self._hashes else 0

    async def hset(self, key: str, field: str | None = None, value: Any = None, mapping: dict[str, Any] | None = None) -> int:
        bucket = self._hashes.setdefault(key, {})
        added = 0

        if mapping:
            for k, v in mapping.items():
                k_str = str(k)
                if k_str not in bucket:
                    added += 1
                bucket[k_str] = str(v)

        if field is not None:
            field_str = str(field)
            if field_str not in bucket:
                added += 1
            bucket[field_str] = str(value)

        return added

    async def hget(self, key: str, field: str) -> str | None:
        return self._hashes.get(key, {}).get(str(field))

    async def hgetall(self, key: str) -> dict[str, str]:
        return dict(self._hashes.get(key, {}))

    async def expire(self, key: str, _ttl_seconds: int) -> bool:
        # TTL intentionally ignored in local degraded mode.
        return key in self._hashes

    async def zadd(self, key: str, mapping: dict[str, float]) -> int:
        bucket = self._zsets.setdefault(key, {})
        added = 0
        for member, score in mapping.items():
            member_str = str(member)
            if member_str not in bucket:
                added += 1
            bucket[member_str] = float(score)
        return added

    async def zrevrange(self, key: str, start: int, end: int, withscores: bool = False):
        bucket = self._zsets.get(key, {})
        items = sorted(bucket.items(), key=lambda kv: kv[1], reverse=True)
        if end == -1:
            window = items[start:]
        else:
            window = items[start : end + 1]
        if withscores:
            return [(member, float(score)) for member, score in window]
        return [member for member, _ in window]

    async def hincrby(self, key: str, field: str, amount: int = 1) -> int:
        bucket = self._hashes.setdefault(key, {})
        current = int(bucket.get(str(field), "0"))
        current += int(amount)
        bucket[str(field)] = str(current)
        return current


class MemoryService:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self.mongo: Optional[AsyncIOMotorClient] = None
        self.qdrant: Optional[AsyncQdrantClient] = None
        self.postgres: Optional[asyncpg.Pool] = None
        raw_namespace = (
            os.getenv("MEMORY_NAMESPACE", "").strip()
            or os.getenv("HARNESS_NAMESPACE", "").strip()
        )
        self.memory_namespace = re.sub(r"[^a-zA-Z0-9_-]+", "-", raw_namespace).strip("-").lower()
        mongo_db_base = os.getenv("AETHER_MONGO_DB", "aether_memory")
        # Mongo bootstrap is DB-scoped in mongo-mem/aether-init.js. Keep the DB name
        # stable and namespace documents instead of inventing new per-namespace DBs
        # that have no user/role bootstrap.
        self.mongo_db_name = self._normalize_db_name(mongo_db_base)
        self.mongo_agent_id = self._normalize_agent_id(
            os.getenv("MEMORY_AGENT_ID", "").strip()
            or os.getenv("AGENT_ID", "").strip()
            or os.getenv("AGENT_NAME", "AetherOps Agent").strip()
        )
        self.embed_url = os.getenv("BGE_EMBED_URL", "https://embed.aetherpro.us/v1/embeddings")
        self.rerank_url = os.getenv("BGE_RERANK_URL", "https://embed.aetherpro.us/rerank")
        self.embed_model = os.getenv("BGE_EMBED_MODEL", "bge-m3")

        # Session tracking
        self.current_session_id: Optional[str] = None
        self.session_start_time: Optional[datetime] = None
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self._identity_docs_cache: dict[str, str] = {}
        self._identity_docs_loaded = False
        self._identity_docs_digest = ""
        self.degraded_mode = False

    async def connect(self):
        """Initialize all connections."""
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            print("[Memory] Connecting to Redis...")
            self.redis = redis.from_url(redis_url, decode_responses=True)
            await self.redis.ping()
            print("[Memory] Redis connected")
        except Exception as exc:
            print(f"[Memory] Redis unavailable ({exc}). Falling back to in-process memory store.")
            self.redis = _InMemoryRedis()  # type: ignore[assignment]
            self.degraded_mode = True

        mongo_uri = os.getenv("AETHER_MONGO_URI", "mongodb://localhost:27017/aether_memory")
        try:
            print("[Memory] Connecting to MongoDB...")
            self.mongo = AsyncIOMotorClient(mongo_uri)
            await self.mongo.admin.command("ping")
            print("[Memory] MongoDB connected")
        except Exception as exc:
            print(f"[Memory] MongoDB unavailable ({exc}). Continuing without Mongo persistence.")
            self.mongo = None
            self.degraded_mode = True

        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
        try:
            print("[Memory] Connecting to Qdrant...")
            self.qdrant = AsyncQdrantClient(host=qdrant_host, port=qdrant_port)
            await self.qdrant.get_collections()
            print("[Memory] Qdrant connected")
        except Exception as exc:
            print(f"[Memory] Qdrant unavailable ({exc}). Continuing without vector memory.")
            self.qdrant = None
            self.degraded_mode = True

        postgres_dsn = os.getenv("POSTGRES_DSN", "postgresql://localhost:5432/postgres")
        postgres_schema = os.getenv("POSTGRES_SCHEMA", "").strip()
        try:
            print("[Memory] Connecting to PostgreSQL...")
            pool_kwargs: dict[str, Any] = {"min_size": 1, "max_size": 5}
            if postgres_schema:
                pool_kwargs["server_settings"] = {"search_path": f"{postgres_schema},public"}
            self.postgres = await asyncpg.create_pool(postgres_dsn, **pool_kwargs)
            print("[Memory] PostgreSQL connected")
        except Exception as exc:
            print(f"[Memory] PostgreSQL unavailable ({exc}). Continuing without relational memory.")
            self.postgres = None
            self.degraded_mode = True

        mode = "degraded" if self.degraded_mode else "full"
        namespace_label = self.memory_namespace or "default"
        print(
            f"[Memory] Memory service initialized ({mode} mode) "
            f"[namespace={namespace_label} mongo_db={self.mongo_db_name}]"
        )

    async def close(self):
        """Close all connections."""
        if self.redis:
            await self.redis.aclose()
        if self.mongo:
            self.mongo.close()
        if self.postgres:
            await self.postgres.close()
        if self.qdrant:
            try:
                await self.qdrant.close()
            except Exception:
                pass
        print("[Memory] All connections closed")

    async def start_session(self, session_id: str):
        """Start a new session in Redis."""
        self.current_session_id = session_id
        self.session_start_time = datetime.utcnow()
        self.total_input_tokens = 0
        self.total_output_tokens = 0

        # Initialize session in Redis
        session_key = self._key_working_session(session_id)
        exists = await self.redis.exists(session_key)
        if not exists:
            # New session - create empty session data
            await self.redis.hset(session_key, mapping={
                "created_at": datetime.utcnow().isoformat(),
                "messages": "[]",
                "context": "",
                "episode_id": ""
            })
            await self.redis.expire(session_key, 86400 * 7)  # 7 days TTL
        await self._initialize_session_state(session_id)

        print(f"[Memory] Session started: {session_id}")

    async def get_messages(self, session_id: str) -> list:
        """Load messages from Redis for a session."""
        session_key = self._key_working_session(session_id)
        messages_json = await self.redis.hget(session_key, "messages")
        if messages_json:
            try:
                return json.loads(messages_json)
            except json.JSONDecodeError:
                return []
        return []

    async def save_messages(self, session_id: str, messages: list):
        """Save messages to Redis for a session."""
        session_key = self._key_working_session(session_id)
        await self.redis.hset(session_key, "messages", json.dumps(messages))

        # Also update the working set index
        await self.redis.zadd(self._key_working_sessions_index(), {session_id: datetime.utcnow().timestamp()})

    def _normalize_session_member(self, member: str) -> tuple[str, str]:
        """Return (session_id, redis_hash_key) from zset member format."""
        session_id = member
        for prefix in (self._key_prefix("working:"), "working:"):
            if session_id.startswith(prefix):
                session_id = session_id[len(prefix):]
                break
        return session_id, self._key_working_session(session_id)

    async def list_sessions(self, limit: int = 50) -> list[dict[str, Any]]:
        """List recent sessions tracked in Redis."""
        limit = max(1, min(limit, 500))
        rows = await self.redis.zrevrange(self._key_working_sessions_index(), 0, limit - 1, withscores=True)
        out: list[dict[str, Any]] = []

        for member, score in rows:
            session_id, session_key = self._normalize_session_member(str(member))
            session_data = await self.redis.hgetall(session_key)
            messages_json = session_data.get("messages", "[]")
            try:
                messages = json.loads(messages_json)
            except json.JSONDecodeError:
                messages = []

            title = "New conversation"
            for msg in reversed(messages):
                if msg.get("role") != "user":
                    continue
                content = msg.get("content")
                texts: list[str] = []
                if isinstance(content, str) and content.strip():
                    texts = [content.strip()]
                elif isinstance(content, list):
                    texts = [
                        str(block.get("text", "")).strip()
                        for block in content
                        if isinstance(block, dict) and block.get("type") == "text"
                    ]

                if not texts:
                    continue

                candidate = next(
                    (
                        text for text in reversed(texts)
                        if text
                        and not text.startswith("[File content from ")
                        and not text.startswith("[Image attachment: ")
                        and not text.startswith("[Compacted conversation summary")
                        and "## Tool Execution Complete" not in text
                    ),
                    "",
                )
                if candidate:
                    title = candidate[:80]
                    break

            out.append(
                {
                    "id": session_id,
                    "title": title,
                    "updated_at": int(float(score) * 1000),
                    "message_count": len(messages),
                }
            )

        return out

    def _message_to_text(self, msg: dict[str, Any]) -> str:
        role = str(msg.get("role", "unknown"))
        content = msg.get("content")

        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            parts: list[str] = []
            for block in content:
                if not isinstance(block, dict):
                    parts.append(str(block))
                    continue
                block_type = block.get("type")
                if block_type == "text":
                    parts.append(str(block.get("text", "")))
                elif block_type == "thinking":
                    parts.append("[thinking omitted]")
                elif block_type == "tool_use":
                    parts.append(f"[tool_call] {block.get('tool_name') or block.get('name')}")
                elif block_type == "tool_result":
                    parts.append(f"[tool_result] {str(block.get('content') or block.get('result') or '')[:220]}")
            text = "\n".join(part for part in parts if part)
        else:
            text = str(content)

        text = re.sub(r"\s+", " ", text).strip()
        return f"{role}: {text}" if text else f"{role}: (empty)"

    def _build_history_summary(self, messages: list[dict[str, Any]], max_chars: int = 2500) -> str:
        snippets = [self._message_to_text(msg) for msg in messages[-18:]]
        summary = "\n".join(f"- {line[:260]}" for line in snippets if line)
        if len(summary) > max_chars:
            return summary[:max_chars] + "\n- [summary truncated]"
        return summary

    async def prepare_messages_for_model(
        self,
        messages: list[dict[str, Any]],
        *,
        max_chars: int | None = None,
    ) -> list[dict[str, Any]]:
        """Compact long message histories to keep context bounded and stable."""
        if max_chars is None:
            max_chars = int(os.getenv("MAX_HISTORY_CHARS_FOR_MODEL", "180000"))
        max_chars = max(2000, int(max_chars))
        if not messages:
            return messages

        estimated_chars = len(json.dumps(messages, ensure_ascii=False))
        if estimated_chars <= max_chars:
            return messages

        tail_budget = int(max_chars * 0.65)
        kept_tail: list[dict[str, Any]] = []
        running = 0

        for msg in reversed(messages):
            msg_json = json.dumps(msg, ensure_ascii=False)
            next_size = len(msg_json)
            if kept_tail and running + next_size > tail_budget:
                break
            kept_tail.append(msg)
            running += next_size

        kept_tail.reverse()
        dropped_count = max(0, len(messages) - len(kept_tail))
        dropped_messages = messages[:dropped_count] if dropped_count else []

        if not dropped_messages:
            return messages

        if self.current_session_id:
            await self._increment_compaction_count(self.current_session_id)

        summary_text = self._build_history_summary(dropped_messages)
        summary_msg = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"[Compacted conversation summary of {dropped_count} earlier messages]\n"
                        f"{summary_text}"
                    ),
                }
            ],
        }

        return [summary_msg, *kept_tail]

    def _key_identity_profile(self) -> str:
        return self._key_prefix("agent:identity:profile")

    def _key_user_profile(self) -> str:
        return self._key_prefix("agent:user:profile")

    def _key_bootstrap_state(self) -> str:
        return self._key_prefix("agent:identity:bootstrap")

    def _key_session_state(self, session_id: str) -> str:
        return self._key_prefix(f"agent:session_state:{session_id}")

    def _key_working_session(self, session_id: str) -> str:
        return self._key_prefix(f"working:{session_id}")

    def _key_working_sessions_index(self) -> str:
        return self._key_prefix("working:sessions")

    def _key_prefix(self, key: str) -> str:
        if not self.memory_namespace:
            return key
        return f"{self.memory_namespace}:{key}"

    def _normalize_db_name(self, base_name: str) -> str:
        base = re.sub(r"[^a-zA-Z0-9_-]+", "_", str(base_name or "aether_memory")).strip("_")
        if not base:
            base = "aether_memory"
        return base

    def _normalize_agent_id(self, value: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(value or "agent")).strip("-").lower()
        return cleaned or "agent"

    def _build_episode_document(
        self,
        messages: list[dict[str, Any]],
        duration: float,
        recent_tools: list[str] | None = None,
    ) -> dict[str, Any]:
        history_summary = self._build_history_summary(messages, max_chars=1800)
        raw_excerpt = history_summary[:2000]

        episode = {
            "agent_id": self.mongo_agent_id,
            "namespace": self.memory_namespace or "default",
            "session_id": self.current_session_id,
            "user_id": os.getenv("MEMORY_USER_ID", "operator"),
            "summary": history_summary or f"Session {self.current_session_id} completed with {len(messages)} messages.",
            "raw_excerpt": raw_excerpt,
            "embedding": [],
            "tags": [],
            "tools_used": list(recent_tools or []),
            "importance": 0.5,
            "created_at": self.session_start_time,
            "ended_at": datetime.utcnow(),
            "duration_seconds": duration,
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "message_count": len(messages),
            "messages": messages[:50],
        }
        return episode

    def _identity_dirs(self) -> list[Path]:
        raw = os.getenv("AGENT_IDENTITY_DIR", "").strip()
        candidates: list[Path] = []
        if raw:
            candidates.append(Path(raw).expanduser())

        here = Path(__file__).resolve()
        candidates.append(here.parents[3] / "agent_identity")  # repo-root sibling
        candidates.append(here.parents[2] / "agent_identity")  # backend-local fallback
        return candidates

    def _compact_doc(self, text: str, *, max_lines: int = 6, max_chars: int = 520) -> str:
        lines = []
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith(("```", "---")):
                continue
            if line.startswith("#"):
                line = line.lstrip("#").strip()
            line = re.sub(r"\s+", " ", line).strip()
            if not line:
                continue
            if len(line) > 160:
                line = line[:160].rstrip() + "..."
            lines.append(line)
            if len(lines) >= max_lines:
                break
        compact = " | ".join(lines)
        if len(compact) > max_chars:
            return compact[:max_chars].rstrip() + "..."
        return compact

    async def _load_identity_docs(self) -> dict[str, str]:
        if self._identity_docs_loaded and self._identity_docs_cache:
            return self._identity_docs_cache

        filenames = [
            "AETHER_IDENTITY.md",
            "AETHER_USER.md",
            "AETHER_ESSENCE.md",
            "AETHER_HEARTBEAT.md",
            "AETHER_BOOTSTRAP.md",
        ]
        docs: dict[str, str] = {}
        for directory in self._identity_dirs():
            if not directory.exists() or not directory.is_dir():
                continue
            for filename in filenames:
                path = directory / filename
                if not path.exists():
                    continue
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                docs[filename] = self._compact_doc(text)
            if docs:
                break

        self._identity_docs_cache = docs
        digest = "\n".join(f"{k}:{v}" for k, v in sorted(docs.items()))
        self._identity_docs_digest = digest[:2000]
        self._identity_docs_loaded = True
        return docs

    async def get_identity_profile(self) -> dict[str, str]:
        raw = await self.redis.hgetall(self._key_identity_profile())
        return {str(k): str(v) for k, v in raw.items()}

    async def get_user_profile(self) -> dict[str, str]:
        raw = await self.redis.hgetall(self._key_user_profile())
        return {str(k): str(v) for k, v in raw.items()}

    async def save_identity_profile(self, payload: dict[str, str]) -> None:
        if not payload:
            return
        clean = {k: str(v).strip() for k, v in payload.items() if str(v).strip()}
        if not clean:
            return
        await self.redis.hset(self._key_identity_profile(), mapping=clean)

    async def save_user_profile(self, payload: dict[str, str]) -> None:
        if not payload:
            return
        clean = {k: str(v).strip() for k, v in payload.items() if str(v).strip()}
        if not clean:
            return
        await self.redis.hset(self._key_user_profile(), mapping=clean)

    async def _initialize_session_state(self, session_id: str) -> None:
        key = self._key_session_state(session_id)
        if await self.redis.exists(key):
            return
        await self.redis.hset(
            key,
            mapping={
                "created_at": datetime.utcnow().isoformat(),
                "status": "active",
                "goal": "",
                "done_count": "0",
                "total_tool_calls": "0",
                "compaction_count": "0",
                "recent_tools": "[]",
                "last_summary": "",
                "next_step": "",
                "build_plan_required": "false",
                "build_plan_status": "none",
                "build_plan_auto_approve": "false",
                "build_plan_summary": "",
                "build_plan_requested_at": "",
                "last_user_message_at": "",
                "last_agent_run_at": "",
                "loaded_tool_schemas": "[]",
            },
        )
        await self.redis.expire(key, 86400 * 14)

    async def _increment_compaction_count(self, session_id: str) -> None:
        key = self._key_session_state(session_id)
        await self._initialize_session_state(session_id)
        await self.redis.hincrby(key, "compaction_count", 1)

    async def get_session_state(self, session_id: str) -> dict[str, Any]:
        key = self._key_session_state(session_id)
        await self._initialize_session_state(session_id)
        data = await self.redis.hgetall(key)
        state: dict[str, Any] = {str(k): v for k, v in data.items()}
        for int_key in ("done_count", "total_tool_calls", "compaction_count"):
            try:
                state[int_key] = int(state.get(int_key, 0))
            except Exception:
                state[int_key] = 0
        recent_raw = state.get("recent_tools", "[]")
        try:
            parsed = json.loads(recent_raw)
            state["recent_tools"] = parsed if isinstance(parsed, list) else []
        except Exception:
            state["recent_tools"] = []
        loaded_tools_raw = state.get("loaded_tool_schemas", "[]")
        try:
            parsed_loaded = json.loads(loaded_tools_raw)
            state["loaded_tool_schemas"] = parsed_loaded if isinstance(parsed_loaded, list) else []
        except Exception:
            state["loaded_tool_schemas"] = []
        return state

    async def update_session_state(self, session_id: str, payload: dict[str, Any]) -> None:
        if not payload:
            return
        await self._initialize_session_state(session_id)
        key = self._key_session_state(session_id)

        update: dict[str, str] = {}
        if "goal" in payload and str(payload["goal"]).strip():
            update["goal"] = str(payload["goal"]).strip()[:600]
        if "status" in payload and str(payload["status"]).strip():
            update["status"] = str(payload["status"]).strip()[:40]
        if "last_summary" in payload:
            update["last_summary"] = str(payload.get("last_summary") or "").strip()[:1000]
        if "next_step" in payload:
            update["next_step"] = str(payload.get("next_step") or "").strip()[:600]
        if "done_count" in payload:
            try:
                update["done_count"] = str(max(0, int(payload["done_count"])))
            except Exception:
                pass
        if "recent_tools" in payload and isinstance(payload["recent_tools"], list):
            recent = [str(t).strip() for t in payload["recent_tools"] if str(t).strip()]
            update["recent_tools"] = json.dumps(recent[-8:])
        if "total_tool_calls" in payload:
            try:
                update["total_tool_calls"] = str(max(0, int(payload["total_tool_calls"])))
            except Exception:
                pass
        if "build_plan_required" in payload:
            update["build_plan_required"] = "true" if bool(payload.get("build_plan_required")) else "false"
        if "build_plan_auto_approve" in payload:
            update["build_plan_auto_approve"] = "true" if bool(payload.get("build_plan_auto_approve")) else "false"
        if "build_plan_status" in payload:
            status = str(payload.get("build_plan_status") or "").strip().lower()
            if status in {"none", "pending", "approved"}:
                update["build_plan_status"] = status
        if "build_plan_summary" in payload:
            update["build_plan_summary"] = str(payload.get("build_plan_summary") or "").strip()[:1200]
        if "build_plan_requested_at" in payload:
            update["build_plan_requested_at"] = str(payload.get("build_plan_requested_at") or "").strip()[:80]
        if "last_user_message_at" in payload:
            update["last_user_message_at"] = str(payload.get("last_user_message_at") or "").strip()[:80]
        if "last_agent_run_at" in payload:
            update["last_agent_run_at"] = str(payload.get("last_agent_run_at") or "").strip()[:80]
        if "loaded_tool_schemas" in payload and isinstance(payload["loaded_tool_schemas"], list):
            loaded_tools = [str(name).strip() for name in payload["loaded_tool_schemas"] if str(name).strip()]
            update["loaded_tool_schemas"] = json.dumps(loaded_tools[-16:])

        if update:
            await self.redis.hset(key, mapping=update)
            await self.redis.expire(key, 86400 * 14)

    async def register_tools_for_session(self, session_id: str, tool_names: list[str]) -> None:
        names = [str(name).strip() for name in tool_names if str(name).strip()]
        if not names:
            return
        state = await self.get_session_state(session_id)
        recent = [*state.get("recent_tools", []), *names][-8:]
        await self.update_session_state(
            session_id,
            {
                "recent_tools": recent,
                "total_tool_calls": int(state.get("total_tool_calls", 0)) + len(names),
            },
        )

    async def load_tool_schemas_for_session(self, session_id: str, tool_names: list[str]) -> list[str]:
        names = [str(name).strip() for name in tool_names if str(name).strip()]
        if not names:
            state = await self.get_session_state(session_id)
            return list(state.get("loaded_tool_schemas", []))
        state = await self.get_session_state(session_id)
        merged: list[str] = []
        for name in [*state.get("loaded_tool_schemas", []), *names]:
            if name and name not in merged:
                merged.append(name)
        merged = merged[-16:]
        await self.update_session_state(session_id, {"loaded_tool_schemas": merged})
        return merged

    async def maybe_capture_user_profile(self, message: str) -> None:
        text = (message or "").strip()
        if not text:
            return
        profile = await self.get_user_profile()
        lower = text.lower()
        update: dict[str, str] = {}

        if not profile.get("name"):
            m = re.search(r"\b(?:i am|i'm|my name is)\s+([A-Za-z][A-Za-z0-9 .'-]{1,40})", text, flags=re.IGNORECASE)
            if m:
                update["name"] = m.group(1).strip()

        if not profile.get("timezone"):
            m = re.search(r"\b(?:timezone|tz)\s*(?:is|:)?\s*([A-Za-z_./+-]{2,60})", text, flags=re.IGNORECASE)
            if m:
                update["timezone"] = m.group(1).strip()

        if not profile.get("context"):
            role_hits = []
            for token in ("founder", "ceo", "cto", "engineer", "developer", "architect", "researcher", "operator"):
                if token in lower:
                    role_hits.append(token)
            if role_hits:
                update["context"] = ", ".join(sorted(set(role_hits)))

        if not profile.get("projects"):
            if "building" in lower or "working on" in lower or "project" in lower:
                update["projects"] = text[:220]

        if update:
            await self.save_user_profile(update)

    async def _ensure_bootstrap_defaults(self) -> None:
        docs = await self._load_identity_docs()
        identity = await self.get_identity_profile()
        user = await self.get_user_profile()

        bootstrap_updates: dict[str, str] = {}
        if self._identity_docs_digest:
            bootstrap_updates["docs_digest"] = self._identity_docs_digest[:1800]
        bootstrap_updates["docs_loaded"] = "true" if docs else "false"

        if not identity:
            seed = {"name": os.getenv("AGENT_NAME", "AetherOps Agent"), "role": "Autonomous execution harness"}
            if docs.get("AETHER_IDENTITY.md"):
                seed["identity_summary"] = docs["AETHER_IDENTITY.md"]
            if docs.get("AETHER_ESSENCE.md"):
                seed["essence_summary"] = docs["AETHER_ESSENCE.md"]
            await self.save_identity_profile(seed)
            bootstrap_updates["agent_seeded"] = "true"

        if not user and docs.get("AETHER_USER.md"):
            await self.save_user_profile({"profile_summary": docs["AETHER_USER.md"]})
            bootstrap_updates["user_seeded"] = "true"

        profile_now = await self.get_user_profile()
        required = ["name", "context", "timezone"]
        missing = [field for field in required if not str(profile_now.get(field) or "").strip()]
        bootstrap_updates["bootstrap_complete"] = "false" if missing else "true"
        bootstrap_updates["bootstrap_missing"] = ",".join(missing)
        await self.redis.hset(self._key_bootstrap_state(), mapping=bootstrap_updates)

    async def build_identity_context_block(self, session_id: str, user_message: str) -> str:
        await self._ensure_bootstrap_defaults()
        await self.maybe_capture_user_profile(user_message)

        identity = await self.get_identity_profile()
        user = await self.get_user_profile()
        state = await self.get_session_state(session_id)
        bootstrap = await self.redis.hgetall(self._key_bootstrap_state())

        lines = ["## Identity & Runtime State"]
        lines.append(
            f"- Agent: {identity.get('name', 'AetherOps Agent')} | Role: {identity.get('role', 'Autonomous execution harness')}"
        )

        user_name = user.get("name") or "unknown"
        user_context = user.get("context") or "unknown"
        user_tz = user.get("timezone") or "unknown"
        lines.append(f"- Operator: {user_name} | Function: {user_context} | TZ: {user_tz}")

        if user.get("projects"):
            lines.append(f"- Operator priorities: {str(user.get('projects'))[:220]}")

        goal = str(state.get("goal") or "").strip() or "(infer from latest user request)"
        lines.append(
            "- Session: "
            f"status={state.get('status', 'active')} | "
            f"goal={goal[:200]} | "
            f"done={state.get('done_count', 0)} | "
            f"tools={state.get('total_tool_calls', 0)} | "
            f"compactions={state.get('compaction_count', 0)}"
        )

        recent = state.get("recent_tools") or []
        if recent:
            lines.append(f"- Recent tools: {', '.join(recent[-5:])}")
        if state.get("next_step"):
            lines.append(f"- Next step (working): {str(state.get('next_step'))[:220]}")

        missing = [s for s in str(bootstrap.get("bootstrap_missing", "")).split(",") if s]
        bootstrap_complete = str(bootstrap.get("bootstrap_complete", "false")).lower() == "true"
        if not bootstrap_complete:
            lines.append(
                "- Onboarding mode: briefly ask for missing profile fields "
                f"({', '.join(missing) if missing else 'name/context/timezone'}) while still executing the main task."
            )
            lines.append(
                "- Onboarding rule: ask at most one concise onboarding question per response to avoid blocking workflow."
            )

        return "\n".join(lines)

    async def build_context(self, user_message: str) -> str:
        """Build contextual memory from relevant past episodes."""
        if not self.current_session_id:
            return ""

        context_parts = []

        # Get recent sessions from Redis
        recent_sessions = await self.redis.zrevrange(self._key_working_sessions_index(), 0, 4, withscores=True)

        relevant_context = []

        for raw_member, _ in recent_sessions:
            member = str(raw_member)
            session_id, session_key = self._normalize_session_member(member)
            if session_id == self.current_session_id:
                continue

            # Get messages from this session
            messages_json = await self.redis.hget(session_key, "messages")
            if messages_json:
                try:
                    messages = json.loads(messages_json)
                    # Get the first user message as title
                    title = "Previous conversation"
                    for msg in messages:
                        if msg.get("role") == "user":
                            content = msg.get("content", "")
                            if isinstance(content, list):
                                for c in content:
                                    if c.get("type") == "text":
                                        title = c.get("text", "")[:50]
                                        break
                            break

                    # Get last assistant response for context
                    last_response = ""
                    for msg in reversed(messages):
                        if msg.get("role") == "assistant":
                            content = msg.get("content", "")
                            if isinstance(content, list):
                                for c in content:
                                    if c.get("type") == "text":
                                        last_response = c.get("text", "")[:200]
                                        break
                            break

                    if title or last_response:
                        relevant_context.append({
                            "session": session_id,
                            "title": title,
                            "summary": last_response
                        })
                except json.JSONDecodeError:
                    pass

        if relevant_context:
            context_parts.append("## Relevant Past Context\n")
            for ctx in relevant_context[:3]:
                context_parts.append(f"- Session {ctx['session'][:8]}...: {ctx['title']}")
                if ctx['summary']:
                    context_parts.append(f"  Last: {ctx['summary']}...")

        return "\n".join(context_parts)

    def get_core_prompt_block(self) -> str:
        """Return the core system prompt block for memory awareness."""
        return """
## Memory Guidelines
- You have access to context from previous relevant conversations shown above
- Use this context to maintain continuity in ongoing discussions
- Do not repeat information the user has already provided
- Be aware of ongoing topics from previous messages in this session
- Continuously maintain a concise session state: goal, completed steps, next step, and recent tool outcomes.
- Keep state compact and factual so compaction events do not break continuity.
"""

    async def record_tokens(self, input_tokens: int = 0, output_tokens: int = 0):
        """Record token usage for the current session."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

        if self.current_session_id:
            session_key = self._key_working_session(self.current_session_id)
            await self.redis.hincrby(session_key, "input_tokens", input_tokens)
            await self.redis.hincrby(session_key, "output_tokens", output_tokens)

    async def end_session(self, provider_client=None):
        """End the session and record episode to MongoDB."""
        if not self.current_session_id or not self.session_start_time:
            return

        session_key = self._key_working_session(self.current_session_id)

        # Get session data
        session_data = await self.redis.hgetall(session_key)

        # Calculate duration
        duration = (datetime.utcnow() - self.session_start_time).total_seconds()

        # Get messages
        messages_json = session_data.get("messages", "[]")
        try:
            messages = json.loads(messages_json)
        except json.JSONDecodeError:
            messages = []

        state = await self.get_session_state(self.current_session_id)
        episode = self._build_episode_document(
            messages,
            duration,
            recent_tools=list(state.get("recent_tools") or []),
        )

        episode_id = ""
        if self.mongo:
            try:
                db = self.mongo[self.mongo_db_name]
                result = await db.episodes.insert_one(episode)
                episode_id = str(result.inserted_id)
                await self.redis.hset(session_key, "episode_id", episode_id)
            except Exception as exc:
                print(f"[Memory] Episode persistence skipped ({exc})")

        print(
            f"[Memory] Session ended. Episode: {episode_id or 'n/a'}, "
            f"Tokens: {self.total_input_tokens}/{self.total_output_tokens}"
        )

        # Reset session tracking
        self.current_session_id = None
        self.session_start_time = None
        self.total_input_tokens = 0
        self.total_output_tokens = 0


# Global service instance
_memory_service: Optional[MemoryService] = None


async def get_memory_service() -> MemoryService:
    """Get or create the global memory service instance."""
    global _memory_service

    if _memory_service is None:
        _memory_service = MemoryService()
        await _memory_service.connect()

    return _memory_service
