"""
═══════════════════════════════════════════════════════════════════════
AETHER-MAX MEMORY SERVICE
═══════════════════════════════════════════════════════════════════════
Wires together:
  - Redis Stack  → Working memory (active session, TTL-based)
  - MongoDB      → Document store (episodes, knowledge, procedures)
  - Qdrant       → Vector index (ANN search via HNSW)
  - BGE Embed    → https://embed.aetherpro.us/v1/embeddings (bge-m3, 1024-dim)
  - BGE Rerank   → https://embed.aetherpro.us/rerank
  - PostgreSQL   → Audit log, sessions, token usage, core memory

USAGE:
  from backend.memory.service import MemoryService
  memory = MemoryService()
  await memory.initialize()

  # Before agent runs
  context = await memory.build_context(session_id, user_message)

  # After agent completes
  await memory.consolidate_session(session_id)
═══════════════════════════════════════════════════════════════════════
"""

import os
import json
import uuid
import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Optional

import httpx
import redis.asyncio as aioredis
from motor.motor_asyncio import AsyncIOMotorClient
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue, SearchRequest
)
import asyncpg
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
EMBED_URL      = os.getenv("BGE_EMBED_URL",   "https://embed.aetherpro.us/v1/embeddings")
RERANK_URL     = os.getenv("BGE_RERANK_URL",  "https://embed.aetherpro.us/rerank")
EMBED_MODEL    = os.getenv("BGE_EMBED_MODEL", "bge-m3")
EMBED_DIM      = int(os.getenv("BGE_EMBED_DIM", "1024"))   # bge-m3 = 1024

REDIS_URL      = os.getenv("REDIS_URL",       "redis://localhost:6379")
MONGO_URI      = os.getenv("AETHER_MONGO_URI", "mongodb://aether_agent:CHANGE_ME@localhost:27018/aether_memory?authSource=aether_memory")
MONGO_DB       = os.getenv("AETHER_MONGO_DB",  "aether_memory")
QDRANT_HOST    = os.getenv("QDRANT_HOST",      "localhost")
QDRANT_PORT    = int(os.getenv("QDRANT_PORT",  "6333"))
POSTGRES_DSN   = os.getenv("POSTGRES_DSN",     "postgresql://redwatch_ops:PASSWORD@localhost:5432/operations")

# Qdrant collection names
QD_EPISODES    = "aether_episodes"
QD_KNOWLEDGE   = "aether_knowledge"
QD_PROCEDURES  = "aether_procedures"

# Retrieval config
EPISODE_TOP_K_FETCH   = 20   # fetch from Qdrant
EPISODE_TOP_K_RERANK  = 5    # keep after reranking
KNOWLEDGE_TOP_K_FETCH = 15
KNOWLEDGE_TOP_K_RERANK= 4
PROCEDURE_TOP_K_FETCH = 10
PROCEDURE_TOP_K_RERANK= 3

# Working memory TTL
WORKING_MEMORY_TTL_SECONDS = 3600  # 1 hour


# ═══════════════════════════════════════════════════════════════════════
# EMBEDDING + RERANKING CLIENT
# ═══════════════════════════════════════════════════════════════════════

class BGEClient:
    """Thin async client for your BGE embed + rerank endpoints."""

    def __init__(self):
        self._http: Optional[httpx.AsyncClient] = None

    async def initialize(self):
        self._http = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        if self._http:
            await self._http.aclose()

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Embed a list of texts. Returns list of 1024-dim vectors.
        Batches automatically if needed.
        """
        if not texts:
            return []

        # Batch in groups of 32 to avoid timeouts on large inputs
        all_vectors = []
        batch_size = 32
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            resp = await self._http.post(
                EMBED_URL,
                json={"input": batch, "model": EMBED_MODEL}
            )
            resp.raise_for_status()
            data = resp.json()
            # OpenAI-compatible response: data.data[].embedding
            vectors = [item["embedding"] for item in data["data"]]
            all_vectors.extend(vectors)

        return all_vectors

    async def embed_one(self, text: str) -> list[float]:
        """Embed a single text string."""
        vectors = await self.embed([text])
        return vectors[0]

    async def rerank(self, query: str, texts: list[str]) -> list[dict]:
        """
        Rerank texts against a query.
        Returns: [{"index": int, "score": float}, ...] sorted by score desc
        """
        if not texts:
            return []

        resp = await self._http.post(
            RERANK_URL,
            json={"query": query, "texts": texts}
        )
        resp.raise_for_status()
        results = resp.json()
        # Already returns [{index, score}] sorted by score desc
        return sorted(results, key=lambda x: x["score"], reverse=True)


# ═══════════════════════════════════════════════════════════════════════
# WORKING MEMORY  (Redis Stack)
# ═══════════════════════════════════════════════════════════════════════

class WorkingMemory:
    """
    Fast in-flight session state stored in Redis.
    Key pattern: working:{session_id}
    Stores: messages[], agent_id, user_id, model, started_at, metadata
    """

    def __init__(self, redis_url: str):
        self._url = redis_url
        self._redis: Optional[aioredis.Redis] = None

    async def initialize(self):
        self._redis = await aioredis.from_url(
            self._url, encoding="utf-8", decode_responses=True
        )
        logger.info("WorkingMemory: Redis connected")

    async def close(self):
        if self._redis:
            await self._redis.aclose()

    def _key(self, session_id: str) -> str:
        return f"working:{session_id}"

    async def create_session(
        self,
        session_id: str,
        agent_id: str = "aether-max",
        user_id: str = "cory",
        model: str = "MiniMax-M2.5"
    ) -> None:
        data = {
            "session_id": session_id,
            "agent_id": agent_id,
            "user_id": user_id,
            "model": model,
            "messages": json.dumps([]),
            "started_at": datetime.now(timezone.utc).isoformat(),
            "tool_call_count": "0",
            "iteration_count": "0",
            "input_tokens": "0",
            "output_tokens": "0",
        }
        await self._redis.hset(self._key(session_id), mapping=data)
        await self._redis.expire(self._key(session_id), WORKING_MEMORY_TTL_SECONDS)
        logger.debug(f"WorkingMemory: created session {session_id}")

    async def get_messages(self, session_id: str) -> list:
        raw = await self._redis.hget(self._key(session_id), "messages")
        if raw is None:
            return []
        return json.loads(raw)

    async def set_messages(self, session_id: str, messages: list) -> None:
        await self._redis.hset(
            self._key(session_id), "messages", json.dumps(messages)
        )
        # Refresh TTL on activity
        await self._redis.expire(self._key(session_id), WORKING_MEMORY_TTL_SECONDS)

    async def get_session(self, session_id: str) -> Optional[dict]:
        data = await self._redis.hgetall(self._key(session_id))
        if not data:
            return None
        data["messages"] = json.loads(data.get("messages", "[]"))
        return data

    async def increment_counters(
        self,
        session_id: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        tool_calls: int = 0,
        iterations: int = 0,
    ) -> None:
        pipe = self._redis.pipeline()
        if input_tokens:
            pipe.hincrby(self._key(session_id), "input_tokens", input_tokens)
        if output_tokens:
            pipe.hincrby(self._key(session_id), "output_tokens", output_tokens)
        if tool_calls:
            pipe.hincrby(self._key(session_id), "tool_call_count", tool_calls)
        if iterations:
            pipe.hincrby(self._key(session_id), "iteration_count", iterations)
        await pipe.execute()

    async def delete_session(self, session_id: str) -> None:
        await self._redis.delete(self._key(session_id))

    async def session_exists(self, session_id: str) -> bool:
        return bool(await self._redis.exists(self._key(session_id)))


# ═══════════════════════════════════════════════════════════════════════
# EPISODIC MEMORY  (MongoDB + Qdrant + BGE)
# ═══════════════════════════════════════════════════════════════════════

class EpisodicMemory:
    """
    Stores summaries of completed conversations.
    MongoDB holds the full document.
    Qdrant holds the vector for ANN search.
    BGE reranker narrows results.
    """

    def __init__(self, mongo_db, qdrant: AsyncQdrantClient, bge: BGEClient):
        self._col = mongo_db["episodes"]
        self._qdrant = qdrant
        self._bge = bge

    async def initialize(self):
        """Ensure Qdrant collection exists."""
        collections = await self._qdrant.get_collections()
        names = [c.name for c in collections.collections]
        if QD_EPISODES not in names:
            await self._qdrant.create_collection(
                collection_name=QD_EPISODES,
                vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE)
            )
            logger.info(f"Qdrant: created collection {QD_EPISODES}")

    async def write(
        self,
        session_id: str,
        agent_id: str,
        user_id: str,
        summary: str,
        raw_excerpt: str = "",
        tags: list[str] = None,
        tools_used: list[str] = None,
        importance: float = 0.5,
    ) -> str:
        """
        Write a completed session to episodic memory.
        Returns the MongoDB _id as string.
        """
        tags = tags or []
        tools_used = tools_used or []

        # Generate embedding
        vector = await self._bge.embed_one(summary)

        # Write to MongoDB
        doc = {
            "agent_id": agent_id,
            "session_id": session_id,
            "user_id": user_id,
            "summary": summary,
            "raw_excerpt": raw_excerpt[:2000],   # cap at 2K chars
            "embedding": vector,
            "tags": tags,
            "tools_used": tools_used,
            "importance": importance,
            "created_at": datetime.now(timezone.utc),
        }
        result = await self._col.insert_one(doc)
        mongo_id = str(result.inserted_id)

        # Write to Qdrant
        await self._qdrant.upsert(
            collection_name=QD_EPISODES,
            points=[PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "mongo_id": mongo_id,
                    "agent_id": agent_id,
                    "session_id": session_id,
                    "tags": tags,
                    "importance": importance,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            )]
        )

        logger.info(f"EpisodicMemory: wrote episode {mongo_id} for session {session_id}")
        return mongo_id

    async def search(
        self,
        query: str,
        agent_id: str = "aether-max",
        top_k: int = EPISODE_TOP_K_RERANK,
    ) -> list[dict]:
        """
        Search episodic memory for relevant past events.
        Returns list of episode dicts, reranked.
        """
        # 1. Embed query
        query_vec = await self._bge.embed_one(query)

        # 2. ANN search in Qdrant
        results = await self._qdrant.search(
            collection_name=QD_EPISODES,
            query_vector=query_vec,
            query_filter=Filter(
                must=[FieldCondition(key="agent_id", match=MatchValue(value=agent_id))]
            ),
            limit=EPISODE_TOP_K_FETCH,
            with_payload=True,
        )

        if not results:
            return []

        # 3. Fetch full docs from MongoDB
        mongo_ids = [r.payload["mongo_id"] for r in results]
        from bson import ObjectId
        docs_cursor = self._col.find(
            {"_id": {"$in": [ObjectId(mid) for mid in mongo_ids]}}
        )
        docs = {str(d["_id"]): d async for d in docs_cursor}

        # 4. Build texts for reranking
        ordered_docs = []
        texts_for_rerank = []
        for r in results:
            doc = docs.get(r.payload["mongo_id"])
            if doc:
                ordered_docs.append(doc)
                texts_for_rerank.append(doc["summary"])

        if not texts_for_rerank:
            return []

        # 5. BGE rerank
        rerank_results = await self._bge.rerank(query, texts_for_rerank)

        # 6. Return top_k reranked docs
        top_docs = []
        for rr in rerank_results[:top_k]:
            doc = ordered_docs[rr["index"]]
            top_docs.append({
                "summary": doc["summary"],
                "tags": doc.get("tags", []),
                "tools_used": doc.get("tools_used", []),
                "importance": doc.get("importance", 0.5),
                "created_at": doc["created_at"].isoformat() if hasattr(doc["created_at"], "isoformat") else str(doc["created_at"]),
                "rerank_score": rr["score"],
                "session_id": doc["session_id"],
            })

        return top_docs


# ═══════════════════════════════════════════════════════════════════════
# SEMANTIC MEMORY  (MongoDB + Qdrant + BGE)
# ═══════════════════════════════════════════════════════════════════════

class SemanticMemory:
    """
    Accumulated facts, entities, user preferences.
    Distilled from episodes over time.
    """

    def __init__(self, mongo_db, qdrant: AsyncQdrantClient, bge: BGEClient):
        self._col = mongo_db["knowledge"]
        self._qdrant = qdrant
        self._bge = bge

    async def initialize(self):
        collections = await self._qdrant.get_collections()
        names = [c.name for c in collections.collections]
        if QD_KNOWLEDGE not in names:
            await self._qdrant.create_collection(
                collection_name=QD_KNOWLEDGE,
                vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE)
            )
            logger.info(f"Qdrant: created collection {QD_KNOWLEDGE}")

        # Embed any seed knowledge that has empty embeddings
        await self._embed_seed_knowledge()

    async def _embed_seed_knowledge(self):
        """Embed any MongoDB knowledge docs that have empty embedding arrays."""
        cursor = self._col.find({"embedding": {"$size": 0}})
        async for doc in cursor:
            fact_text = f"{doc['entity']}: {doc['fact']}"
            vector = await self._bge.embed_one(fact_text)

            # Update MongoDB
            await self._col.update_one(
                {"_id": doc["_id"]},
                {"$set": {"embedding": vector, "updated_at": datetime.now(timezone.utc)}}
            )

            # Upsert to Qdrant
            await self._qdrant.upsert(
                collection_name=QD_KNOWLEDGE,
                points=[PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "mongo_id": str(doc["_id"]),
                        "agent_id": doc["agent_id"],
                        "entity": doc["entity"],
                        "category": doc.get("category", "general"),
                    }
                )]
            )
            logger.info(f"SemanticMemory: embedded seed knowledge: {doc['entity']}")

    async def upsert_fact(
        self,
        agent_id: str,
        entity: str,
        fact: str,
        category: str = "general",
        confidence: float = 0.8,
        source_episode_id: str = None,
    ) -> str:
        """Write or update a semantic memory fact."""
        fact_text = f"{entity}: {fact}"
        vector = await self._bge.embed_one(fact_text)

        # Check if fact about this entity already exists
        existing = await self._col.find_one(
            {"agent_id": agent_id, "entity": entity}
        )

        now = datetime.now(timezone.utc)
        source_episodes = [source_episode_id] if source_episode_id else []

        if existing:
            # Update existing
            await self._col.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "fact": fact,
                    "embedding": vector,
                    "confidence": confidence,
                    "updated_at": now,
                }, "$addToSet": {"source_episodes": {"$each": source_episodes}}}
            )
            mongo_id = str(existing["_id"])
        else:
            # Insert new
            result = await self._col.insert_one({
                "agent_id": agent_id,
                "entity": entity,
                "fact": fact,
                "embedding": vector,
                "confidence": confidence,
                "source_episodes": source_episodes,
                "category": category,
                "created_at": now,
                "updated_at": now,
            })
            mongo_id = str(result.inserted_id)

        # Upsert to Qdrant
        await self._qdrant.upsert(
            collection_name=QD_KNOWLEDGE,
            points=[PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "mongo_id": mongo_id,
                    "agent_id": agent_id,
                    "entity": entity,
                    "category": category,
                }
            )]
        )
        return mongo_id

    async def search(
        self,
        query: str,
        agent_id: str = "aether-max",
        top_k: int = KNOWLEDGE_TOP_K_RERANK,
    ) -> list[dict]:
        """Search semantic memory for relevant facts."""
        query_vec = await self._bge.embed_one(query)

        results = await self._qdrant.search(
            collection_name=QD_KNOWLEDGE,
            query_vector=query_vec,
            query_filter=Filter(
                must=[FieldCondition(key="agent_id", match=MatchValue(value=agent_id))]
            ),
            limit=KNOWLEDGE_TOP_K_FETCH,
            with_payload=True,
        )

        if not results:
            return []

        mongo_ids = [r.payload["mongo_id"] for r in results]
        from bson import ObjectId
        docs_cursor = self._col.find(
            {"_id": {"$in": [ObjectId(mid) for mid in mongo_ids]}}
        )
        docs = {str(d["_id"]): d async for d in docs_cursor}

        ordered_docs = []
        texts_for_rerank = []
        for r in results:
            doc = docs.get(r.payload["mongo_id"])
            if doc:
                ordered_docs.append(doc)
                texts_for_rerank.append(f"{doc['entity']}: {doc['fact']}")

        if not texts_for_rerank:
            return []

        rerank_results = await self._bge.rerank(query, texts_for_rerank)

        top_docs = []
        for rr in rerank_results[:top_k]:
            doc = ordered_docs[rr["index"]]
            top_docs.append({
                "entity": doc["entity"],
                "fact": doc["fact"],
                "category": doc.get("category", "general"),
                "confidence": doc.get("confidence", 0.8),
                "rerank_score": rr["score"],
            })

        return top_docs


# ═══════════════════════════════════════════════════════════════════════
# CORE MEMORY  (PostgreSQL — always-on)
# ═══════════════════════════════════════════════════════════════════════

class CoreMemory:
    """
    Permanent, curated identity/profile layer.
    Loaded once at startup, cached in memory.
    Injected into every agent system prompt.
    """

    def __init__(self, pg_pool):
        self._pool = pg_pool
        self._cache: list[dict] = []
        self._loaded = False

    async def load(self, agent_id: str = "aether-max") -> list[dict]:
        """Load core memory from Postgres, cache it."""
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT key, value, category, priority
                FROM agent_memory.core_memory
                WHERE agent_id = $1
                ORDER BY priority DESC, category
                """,
                agent_id
            )
        self._cache = [dict(row) for row in rows]
        self._loaded = True
        logger.info(f"CoreMemory: loaded {len(self._cache)} entries")
        return self._cache

    def get_cached(self) -> list[dict]:
        return self._cache

    def format_for_prompt(self) -> str:
        """Format core memory as a system prompt block."""
        if not self._cache:
            return ""

        lines = ["## Core Context (Always Active)"]
        categories = {}
        for item in self._cache:
            cat = item["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(f"- **{item['key']}**: {item['value']}")

        for cat, items in categories.items():
            lines.append(f"\n### {cat.replace('_', ' ').title()}")
            lines.extend(items)

        return "\n".join(lines)

    async def upsert(self, agent_id: str, key: str, value: str, category: str, priority: int = 5) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO agent_memory.core_memory (agent_id, key, value, category, priority)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (agent_id, key) DO UPDATE
                    SET value = EXCLUDED.value,
                        priority = EXCLUDED.priority,
                        updated_at = NOW()
                """,
                agent_id, key, value, category, priority
            )
        # Invalidate cache
        self._loaded = False


# ═══════════════════════════════════════════════════════════════════════
# AUDIT / SESSION LOGGER  (PostgreSQL)
# ═══════════════════════════════════════════════════════════════════════

class AuditLogger:
    def __init__(self, pg_pool):
        self._pool = pg_pool

    async def create_session(self, session_id: str, agent_id: str = "aether-max", user_id: str = "cory", model: str = "MiniMax-M2.5") -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO agent_memory.sessions (session_id, agent_id, user_id, model)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (session_id) DO NOTHING
                """,
                session_id, agent_id, user_id, model
            )

    async def close_session(self, session_id: str, input_tokens: int, output_tokens: int, tool_calls: int, iterations: int) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE agent_memory.sessions
                SET status = 'completed',
                    ended_at = NOW(),
                    total_input_tokens = $2,
                    total_output_tokens = $3,
                    tool_call_count = $4,
                    iteration_count = $5
                WHERE session_id = $1
                """,
                session_id, input_tokens, output_tokens, tool_calls, iterations
            )

    async def update_title(self, session_id: str, title: str) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                "UPDATE agent_memory.sessions SET title = $2 WHERE session_id = $1",
                session_id, title[:255]
            )

    async def log_memory_op(
        self,
        op_type: str,
        session_id: str = None,
        agent_id: str = "aether-max",
        collection: str = None,
        query_text: str = None,
        results_count: int = None,
        latency_ms: int = None,
        tokens_used: int = None,
    ) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO agent_memory.memory_ops
                    (session_id, agent_id, op_type, collection, query_text, results_count, latency_ms, tokens_used)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                session_id, agent_id, op_type, collection, query_text,
                results_count, latency_ms, tokens_used
            )

    async def log_tokens(self, session_id: str, agent_id: str, model: str, input_tokens: int, output_tokens: int, operation: str = "chat", cost_usd: float = None) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO agent_memory.token_usage
                    (session_id, agent_id, model, input_tokens, output_tokens, operation, cost_usd)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                session_id, agent_id, model, input_tokens, output_tokens, operation, cost_usd
            )


# ═══════════════════════════════════════════════════════════════════════
# CONSOLIDATION ENGINE
# Runs after session ends — summarizes, extracts, writes to long-term memory
# ═══════════════════════════════════════════════════════════════════════

class ConsolidationEngine:
    """
    Post-session background worker.
    Summarizes conversation → writes episodic memory.
    Extracts facts → updates semantic memory.
    """

    def __init__(self, episodic: EpisodicMemory, semantic: SemanticMemory, bge: BGEClient):
        self._episodic = episodic
        self._semantic = semantic
        self._bge = bge

    async def consolidate(
        self,
        session_id: str,
        agent_id: str,
        user_id: str,
        messages: list,
        minimax_client,   # the anthropic client pointed at MiniMax
        tool_names_used: list[str] = None,
    ) -> Optional[str]:
        """
        Summarize conversation and write to episodic memory.
        Also extract key facts for semantic memory.
        Returns episode mongo_id.
        """
        if not messages:
            return None

        tool_names_used = tool_names_used or []

        # Build conversation text for summarization
        convo_text = self._format_messages_for_summary(messages)
        if len(convo_text) < 100:
            return None   # too short to be worth storing

        try:
            # ── Step 1: Generate summary via MiniMax (lightweight call, no tools)
            summary_resp = minimax_client.messages.create(
                model="MiniMax-M2.5",
                max_tokens=512,
                messages=[{
                    "role": "user",
                    "content": f"""Summarize this agent conversation in 3-5 sentences. Focus on:
1. What the user was trying to accomplish
2. What tools/actions the agent took
3. The outcome and any key findings
4. Any important facts learned about the user, their projects, or preferences

Conversation:
{convo_text[:6000]}

Write only the summary, no preamble."""
                }]
            )
            summary = summary_resp.content[0].text.strip()

            # ── Step 2: Extract tags
            tags = self._extract_tags(messages, tool_names_used)

            # ── Step 3: Importance scoring (simple heuristic)
            importance = self._score_importance(messages, tool_names_used)

            # ── Step 4: Write episode
            mongo_id = await self._episodic.write(
                session_id=session_id,
                agent_id=agent_id,
                user_id=user_id,
                summary=summary,
                raw_excerpt=convo_text[:1500],
                tags=tags,
                tools_used=tool_names_used,
                importance=importance,
            )

            # ── Step 5: Extract semantic facts (async, non-blocking)
            asyncio.create_task(
                self._extract_semantic_facts(
                    convo_text, summary, agent_id, mongo_id, minimax_client
                )
            )

            logger.info(f"Consolidation: wrote episode {mongo_id} for session {session_id}")
            return mongo_id

        except Exception as e:
            logger.error(f"Consolidation failed for session {session_id}: {e}")
            return None

    def _format_messages_for_summary(self, messages: list) -> str:
        lines = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if isinstance(content, list):
                # Anthropic content blocks
                text_parts = []
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                        elif block.get("type") == "tool_use":
                            text_parts.append(f"[Tool: {block.get('name')}({json.dumps(block.get('input', {}))[:200]})]")
                        elif block.get("type") == "tool_result":
                            result_content = block.get("content", "")
                            if isinstance(result_content, list):
                                result_content = " ".join([c.get("text","") for c in result_content if isinstance(c,dict)])
                            text_parts.append(f"[Result: {str(result_content)[:300]}]")
                    elif hasattr(block, "type"):
                        if block.type == "text":
                            text_parts.append(block.text)
                        elif block.type == "tool_use":
                            text_parts.append(f"[Tool: {block.name}]")
                content = " ".join(text_parts)
            if content and not isinstance(content, str):
                content = str(content)
            if content:
                lines.append(f"{role.upper()}: {content[:500]}")
        return "\n".join(lines)

    def _extract_tags(self, messages: list, tools_used: list[str]) -> list[str]:
        tags = set(tools_used)
        # Add tags based on content keywords
        text = self._format_messages_for_summary(messages).lower()
        tag_keywords = {
            "redwatch": "redwatch", "cmmc": "cmmc", "federal": "federal-contracting",
            "cybersecurity": "cybersecurity", "python": "python", "code": "coding",
            "file": "file-ops", "search": "web-search", "aetherpro": "aetherpro",
            "blackbox": "blackbox-audio", "perceptor": "perceptor",
            "qdrant": "infrastructure", "redis": "infrastructure", "postgres": "infrastructure",
            "minimax": "minimax", "agent": "agent-dev",
        }
        for keyword, tag in tag_keywords.items():
            if keyword in text:
                tags.add(tag)
        return list(tags)[:15]  # cap at 15 tags

    def _score_importance(self, messages: list, tools_used: list[str]) -> float:
        """Heuristic importance score 0.0-1.0."""
        score = 0.3  # baseline

        # More tool calls = more important
        if len(tools_used) > 3:
            score += 0.2
        elif len(tools_used) > 0:
            score += 0.1

        # More messages = more important (longer task)
        msg_count = len([m for m in messages if m.get("role") == "user"])
        if msg_count > 3:
            score += 0.2
        elif msg_count > 1:
            score += 0.1

        # High-value tools
        high_value = {"execute_python", "web_search", "write_file", "run_shell"}
        if any(t in high_value for t in tools_used):
            score += 0.2

        return min(score, 1.0)

    async def _extract_semantic_facts(
        self,
        convo_text: str,
        summary: str,
        agent_id: str,
        episode_id: str,
        minimax_client,
    ) -> None:
        """Extract structured facts from conversation and update semantic memory."""
        try:
            extract_resp = minimax_client.messages.create(
                model="MiniMax-M2.5",
                max_tokens=400,
                messages=[{
                    "role": "user",
                    "content": f"""Extract 0-5 important facts from this conversation that should be remembered long-term.
Only extract facts that are genuinely useful to remember: user preferences, project status, key decisions, technical facts about their systems.
Do NOT extract generic or obvious information.

Respond in JSON format only:
[
  {{"entity": "EntityName", "fact": "The fact to remember", "category": "person|project|preference|domain|infrastructure"}},
  ...
]

If nothing worth remembering, respond: []

Conversation summary: {summary}

Key excerpt: {convo_text[:3000]}"""
                }]
            )

            text = extract_resp.content[0].text.strip()
            # Strip markdown code fences if present
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            text = text.strip()

            facts = json.loads(text)
            if not isinstance(facts, list):
                return

            for fact in facts[:5]:
                if "entity" in fact and "fact" in fact:
                    await self._semantic.upsert_fact(
                        agent_id=agent_id,
                        entity=fact["entity"],
                        fact=fact["fact"],
                        category=fact.get("category", "general"),
                        source_episode_id=episode_id,
                    )
                    logger.info(f"SemanticMemory: extracted fact about '{fact['entity']}'")

        except Exception as e:
            logger.warning(f"Semantic extraction failed: {e}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN MEMORY SERVICE — unified interface for the agent
# ═══════════════════════════════════════════════════════════════════════

class MemoryService:
    """
    Single entry point for all memory operations.
    The agent only needs to interact with this class.
    """

    def __init__(self):
        self.bge          = BGEClient()
        self.working      = WorkingMemory(REDIS_URL)
        self._pg_pool     = None
        self._mongo_db    = None
        self._qdrant      = None
        self.core         = None
        self.episodic     = None
        self.semantic     = None
        self.audit        = None
        self.consolidator = None
        self._initialized = False

    async def initialize(self):
        if self._initialized:
            return

        logger.info("MemoryService: initializing...")

        # BGE
        await self.bge.initialize()

        # Redis
        await self.working.initialize()

        # PostgreSQL
        self._pg_pool = await asyncpg.create_pool(POSTGRES_DSN, min_size=2, max_size=10)
        self.core  = CoreMemory(self._pg_pool)
        self.audit = AuditLogger(self._pg_pool)
        await self.core.load()

        # MongoDB
        mongo_client = AsyncIOMotorClient(MONGO_URI)
        self._mongo_db = mongo_client[MONGO_DB]

        # Qdrant
        self._qdrant = AsyncQdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

        # Sub-services
        self.episodic     = EpisodicMemory(self._mongo_db, self._qdrant, self.bge)
        self.semantic     = SemanticMemory(self._mongo_db, self._qdrant, self.bge)
        self.consolidator = ConsolidationEngine(self.episodic, self.semantic, self.bge)

        # Ensure Qdrant collections exist + embed seed knowledge
        await self.episodic.initialize()
        await self.semantic.initialize()

        self._initialized = True
        logger.info("MemoryService: ✅ fully initialized")

    async def close(self):
        await self.bge.close()
        await self.working.close()
        if self._pg_pool:
            await self._pg_pool.close()
        if self._qdrant:
            await self._qdrant.close()

    # ─────────────────────────────────────────────
    # PRIMARY AGENT INTERFACE
    # ─────────────────────────────────────────────

    async def start_session(self, session_id: str, model: str = "MiniMax-M2.5") -> None:
        """Call this when a new chat session begins."""
        await self.working.create_session(session_id, model=model)
        await self.audit.create_session(session_id, model=model)

    async def build_context(self, session_id: str, user_message: str) -> str:
        """
        Build the memory context block to inject into the system prompt.
        Runs episodic + semantic search in parallel.
        Returns a formatted string to append to the system prompt.
        """
        t0 = time.monotonic()

        # Run searches in parallel
        episode_task = asyncio.create_task(
            self.episodic.search(user_message)
        )
        knowledge_task = asyncio.create_task(
            self.semantic.search(user_message)
        )

        episodes, knowledge = await asyncio.gather(episode_task, knowledge_task)
        latency_ms = int((time.monotonic() - t0) * 1000)

        # Log the memory read
        asyncio.create_task(self.audit.log_memory_op(
            op_type="read_episodic+semantic",
            session_id=session_id,
            collection="episodes+knowledge",
            query_text=user_message[:200],
            results_count=len(episodes) + len(knowledge),
            latency_ms=latency_ms,
        ))

        # Format context block
        blocks = []

        if episodes:
            blocks.append("## Relevant Past Conversations")
            for ep in episodes:
                date_str = ep["created_at"][:10] if ep["created_at"] else "unknown"
                blocks.append(f"- [{date_str}] {ep['summary']}")
                if ep.get("tools_used"):
                    blocks.append(f"  Tools used: {', '.join(ep['tools_used'])}")

        if knowledge:
            blocks.append("\n## Relevant Knowledge")
            for k in knowledge:
                blocks.append(f"- **{k['entity']}**: {k['fact']}")

        if not blocks:
            return ""

        return "\n".join(blocks)

    async def get_messages(self, session_id: str) -> list:
        """Get current session message history."""
        return await self.working.get_messages(session_id)

    async def save_messages(self, session_id: str, messages: list) -> None:
        """Save updated message history back to Redis."""
        await self.working.set_messages(session_id, messages)

    async def record_tokens(self, session_id: str, model: str, input_tokens: int, output_tokens: int, tool_calls: int = 0, iterations: int = 0) -> None:
        """Record token usage for a session turn."""
        await self.working.increment_counters(session_id, input_tokens, output_tokens, tool_calls, iterations)
        # MiniMax M2.5 pricing: $0.15/M input, $1.20/M output (M2.5-lightning pricing)
        cost = (input_tokens / 1_000_000 * 0.15) + (output_tokens / 1_000_000 * 1.20)
        asyncio.create_task(self.audit.log_tokens(
            session_id=session_id, agent_id="aether-max",
            model=model, input_tokens=input_tokens,
            output_tokens=output_tokens, cost_usd=cost
        ))

    async def end_session(self, session_id: str, minimax_client, tool_names_used: list[str] = None) -> None:
        """
        Call when agent finishes responding.
        Closes session in Postgres, triggers background consolidation.
        """
        session = await self.working.get_session(session_id)
        if not session:
            return

        messages = session.get("messages", [])
        input_tokens  = int(session.get("input_tokens", 0))
        output_tokens = int(session.get("output_tokens", 0))
        tool_calls    = int(session.get("tool_call_count", 0))
        iterations    = int(session.get("iteration_count", 0))

        # Update Postgres session record
        await self.audit.close_session(
            session_id, input_tokens, output_tokens, tool_calls, iterations
        )

        # Auto-title from first user message
        if messages:
            first_user = next(
                (m for m in messages if m.get("role") == "user"), None
            )
            if first_user:
                content = first_user.get("content", "")
                if isinstance(content, list):
                    content = " ".join([b.get("text","") for b in content if isinstance(b,dict) and b.get("type")=="text"])
                title = str(content)[:60]
                await self.audit.update_title(session_id, title)

        # Background consolidation — doesn't block the response
        asyncio.create_task(
            self.consolidator.consolidate(
                session_id=session_id,
                agent_id="aether-max",
                user_id="cory",
                messages=messages,
                minimax_client=minimax_client,
                tool_names_used=tool_names_used or [],
            )
        )

    def get_core_prompt_block(self) -> str:
        """Get formatted core memory for system prompt injection."""
        return self.core.format_for_prompt()


# ═══════════════════════════════════════════════════════════════════════
# SINGLETON (import and use this)
# ═══════════════════════════════════════════════════════════════════════

_memory_service: Optional[MemoryService] = None

async def get_memory_service() -> MemoryService:
    global _memory_service
    if _memory_service is None:
        _memory_service = MemoryService()
        await _memory_service.initialize()
    return _memory_service
