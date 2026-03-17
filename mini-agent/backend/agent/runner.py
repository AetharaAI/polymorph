from __future__ import annotations

import os
import asyncio
import json
import re
import ast
import time
import sys
import traceback
from pathlib import Path
from typing import Any, Callable
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.agent.providers import get_provider, provider_metadata
from backend.agent.providers.factory import get_multimodal_audio_provider
from backend.agent.providers.base import BaseLLMProvider, LLMContentBlock
from backend.agent.skills import build_skills_prompt
from backend.agent.telemetry import SessionReplayLogger
from backend.agent.tools import TOOL_DEFINITIONS, dispatch_tool
from backend.agent.tools.manifest import build_tools_prompt_block, get_active_tool_definitions
from backend.agent.tools import file_ops
from backend.config import load_harness_env, resolve_env
from backend.memory import get_memory_service

load_harness_env()

DEFAULT_SYSTEM_PROMPT = """You are Agent-Max, an autonomous AI agent running inside a model-agnostic execution harness.

You must not fabricate facts. If uncertain, say so clearly and verify before concluding.
Prefer primary sources, cite provenance, and state confidence when evidence is weak.
Do not guess the current date or time from model memory. Use the explicit temporal context provided by the harness."""

DEFAULT_EVAL_PROMPT = """## Tool Execution Complete

Evaluate the tool results:
1. Did this materially advance the user's objective?
2. If uncertain, what verification step is required next?
3. Decide next action: continue_same_strategy, revise_query_or_parameters, switch_tools, or conclude_task.
4. Never invent facts. If evidence is insufficient, explicitly say so and verify."""

MODEL_CONTEXT_WINDOW = int(os.getenv("MODEL_CONTEXT_WINDOW", "0") or "0")
MAX_ITERATIONS = int(os.getenv("MAX_AGENT_ITERATIONS", "60"))
MAX_TOOL_CALLS_PER_ITERATION = int(os.getenv("MAX_TOOL_CALLS_PER_ITERATION", "12"))
MAX_TOOL_CALLS_PER_RUN = int(os.getenv("MAX_TOOL_CALLS_PER_RUN", "120"))
AGENT_MAX_TOKENS = int(os.getenv("AGENT_MAX_TOKENS", "16384"))
AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "1.0"))
INCLUDE_THINKING_IN_CONTEXT = os.getenv("INCLUDE_THINKING_IN_CONTEXT", "false").strip().lower() in {"1", "true", "yes", "on"}
MAX_TEXT_BLOCK_CHARS_FOR_CONTEXT = int(os.getenv("MAX_TEXT_BLOCK_CHARS_FOR_CONTEXT", "20000"))
MAX_TOOL_RESULT_CHARS_FOR_CONTEXT = int(os.getenv("MAX_TOOL_RESULT_CHARS_FOR_CONTEXT", "12000"))
STRICT_VERIFICATION_MODE = os.getenv("STRICT_VERIFICATION_MODE", "true").strip().lower() in {"1", "true", "yes", "on"}
ENABLE_REPLAY_LOGS = os.getenv("ENABLE_REPLAY_LOGS", "true").strip().lower() in {"1", "true", "yes", "on"}
INCLUDE_HARNESS_METADATA_IN_PROMPT = os.getenv(
    "AGENT_INCLUDE_HARNESS_METADATA_IN_PROMPT", "false"
).strip().lower() in {"1", "true", "yes", "on"}
DYNAMIC_TOOL_SELECTION_ENABLED = os.getenv(
    "AGENT_DYNAMIC_TOOL_SELECTION", "true"
).strip().lower() in {"1", "true", "yes", "on"}
CONTEXT_WINDOW_FALLBACK_MULTIPLIER = float(os.getenv("CONTEXT_WINDOW_FALLBACK_MULTIPLIER", "2.0"))
CONTEXT_WINDOW_FALLBACK_MIN = int(os.getenv("CONTEXT_WINDOW_FALLBACK_MIN", "8192"))
CONTEXT_WINDOW_MESSAGE_CHAR_RATIO = float(os.getenv("CONTEXT_WINDOW_MESSAGE_CHAR_RATIO", "4.0"))
CONTEXT_WINDOW_OUTPUT_RESERVE = int(os.getenv("CONTEXT_WINDOW_OUTPUT_RESERVE", "256"))
MIN_MESSAGE_HISTORY_CHARS = int(os.getenv("MIN_MESSAGE_HISTORY_CHARS", "4000"))
PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"
AGENTS_RULES_PATH = Path(os.getenv("AGENTS_RULES_PATH", str(Path(__file__).resolve().parents[1] / "AGENTS.md")))
PLAN_APPROVAL_KEYWORDS = tuple(
    s.strip().lower()
    for s in os.getenv("AGENT_PLAN_APPROVAL_KEYWORDS", "approve plan,plan approved,proceed with build,go ahead build").split(",")
    if s.strip()
)
PROJECT_BUILD_KEYWORDS = {
    "build spec",
    "full stack",
    "scaffold",
    "generate project",
    "create project",
    "project structure",
    "phase 1",
    "phase 2",
    "requirements.txt",
    "docker-compose",
    "backend",
    "frontend",
}

VERIFY_KEYWORDS = {
    "latest",
    "current",
    "today",
    "yesterday",
    "price",
    "version",
    "news",
    "report",
    "research",
    "verify",
    "evidence",
    "source",
    "sources",
    "documentation",
    "benchmark",
}


def _parse_iso_datetime(raw: str | None) -> datetime | None:
    text = (raw or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except Exception:
        return None


def _format_elapsed(seconds: float | None) -> str:
    if seconds is None or seconds < 0:
        return "n/a"
    total = int(seconds)
    days, rem = divmod(total, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if hours or days:
        parts.append(f"{hours}h")
    if minutes or hours or days:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    return " ".join(parts)


def _resolve_temporal_timezone(user_timezone: str | None) -> tuple[str, timezone | ZoneInfo]:
    explicit = (user_timezone or "").strip() or resolve_env("AGENT_TIMEZONE", default="").strip()
    if explicit:
        try:
            return explicit, ZoneInfo(explicit)
        except Exception:
            pass
    local = datetime.now().astimezone().tzinfo
    tz_name = getattr(local, "key", None) or str(local or "UTC")
    return tz_name, local or timezone.utc


def _build_temporal_context_block(
    *,
    session_state: dict[str, Any],
    user_timezone: str | None,
    now_utc: datetime,
) -> str:
    tz_name, tz_obj = _resolve_temporal_timezone(user_timezone)
    now_local = now_utc.astimezone(tz_obj)
    session_created_at = _parse_iso_datetime(str(session_state.get("created_at") or ""))
    previous_user_turn = _parse_iso_datetime(str(session_state.get("last_user_message_at") or ""))
    previous_agent_run = _parse_iso_datetime(str(session_state.get("last_agent_run_at") or ""))

    session_age_seconds = (now_utc - session_created_at).total_seconds() if session_created_at else None
    since_previous_user_seconds = (now_utc - previous_user_turn).total_seconds() if previous_user_turn else None
    since_previous_agent_seconds = (now_utc - previous_agent_run).total_seconds() if previous_agent_run else None

    lines = [
        "## Temporal Context",
        f"- utc={now_utc.isoformat()}",
        f"- local={now_local.isoformat()} ({tz_name})",
        f"- unix={int(now_utc.timestamp())}",
        f"- session_created_at_utc={session_created_at.isoformat() if session_created_at else 'n/a'} age={_format_elapsed(session_age_seconds)}",
        f"- previous_user_turn_at_utc={previous_user_turn.isoformat() if previous_user_turn else 'n/a'} elapsed={_format_elapsed(since_previous_user_seconds)}",
        f"- previous_agent_run_at_utc={previous_agent_run.isoformat() if previous_agent_run else 'n/a'} elapsed={_format_elapsed(since_previous_agent_seconds)}",
        "- Use these timestamps for relative dates instead of guessing.",
    ]
    return "\n".join(lines)


async def _build_harness_metadata_block(tool_definitions: list[dict[str, Any]]) -> str:
    memory = await get_memory_service()
    provider = provider_metadata()
    actual = provider.get("actual", {})
    requested = provider.get("requested", {})
    fallbacks = provider.get("fallbacks") or []
    lines = [
        "## Harness Metadata",
        "- Treat this block as authoritative harness self-knowledge for this response.",
        f"- Requested provider/model: {requested.get('provider', 'n/a')} / {requested.get('model', 'n/a')}",
        f"- Actual provider/model: {actual.get('provider', provider.get('provider', 'n/a'))} / {actual.get('model', provider.get('model', 'n/a'))}",
        f"- Tool count this turn: {len(tool_definitions)}",
        f"- Skills registry: {Path(__file__).resolve().parents[1] / 'SKILLS.md'}",
        f"- Memory namespace: {getattr(memory, 'memory_namespace', '') or 'default'}",
        f"- Memory degraded mode: {bool(getattr(memory, 'degraded_mode', False))}",
        f"- Fallback providers configured: {len(fallbacks)}",
        "- If asked what tools or capabilities exist, prefer get_harness_status over guessing.",
    ]
    return "\n".join(lines)


def _load_prompt(path_env: str, default_filename: str, fallback: str) -> str:
    """Load prompt text from env path or backend/prompts directory."""
    env_path = os.getenv(path_env)
    path = Path(env_path) if env_path else (PROMPTS_DIR / default_filename)
    try:
        content = path.read_text(encoding="utf-8").strip()
        return content if content else fallback
    except Exception:
        return fallback


def _load_optional_text(path: Path) -> str:
    try:
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8", errors="ignore").strip()
    except Exception:
        return ""


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on", "auto", "always"}


def _is_project_build_request(user_message: str) -> bool:
    lowered = (user_message or "").lower()
    if any(keyword in lowered for keyword in PROJECT_BUILD_KEYWORDS):
        return True
    return lowered.count("\n") > 12 and any(token in lowered for token in {"api", "auth", "database", "schema", "test"})


def _select_tool_definitions(
    *,
    loaded_tool_names: list[str] | None = None,
) -> list[dict[str, Any]]:
    if not DYNAMIC_TOOL_SELECTION_ENABLED:
        return TOOL_DEFINITIONS
    return get_active_tool_definitions(TOOL_DEFINITIONS, loaded_tool_names=loaded_tool_names)


def _resolve_effective_context_window(provider: Any, requested_max_tokens: int) -> int:
    compat_override = resolve_env("OPENAI_COMPAT_CONTEXT_WINDOW", default="").strip()
    for raw in (compat_override, str(MODEL_CONTEXT_WINDOW or "")):
        try:
            value = int(raw)
        except Exception:
            value = 0
        if value > 0:
            return value

    provider_name = str(getattr(provider, "provider_name", "") or "").lower()
    if "openai_compat" not in provider_name:
        return max(requested_max_tokens * 4, CONTEXT_WINDOW_FALLBACK_MIN)

    fallback_window = max(
        CONTEXT_WINDOW_FALLBACK_MIN,
        int(requested_max_tokens * CONTEXT_WINDOW_FALLBACK_MULTIPLIER),
    )
    return fallback_window


def _history_char_budget_for_iteration(
    *,
    provider: Any,
    system_prompt: str,
    requested_max_tokens: int,
) -> tuple[int, int]:
    context_window = _resolve_effective_context_window(provider, requested_max_tokens)
    configured_cap = int(os.getenv("MAX_HISTORY_CHARS_FOR_MODEL", "180000"))
    input_budget_tokens = max(1024, context_window - requested_max_tokens - CONTEXT_WINDOW_OUTPUT_RESERVE)
    budget_chars = int(input_budget_tokens * CONTEXT_WINDOW_MESSAGE_CHAR_RATIO) - len(system_prompt)
    budget_chars = max(MIN_MESSAGE_HISTORY_CHARS, budget_chars)
    return min(configured_cap, budget_chars), context_window


def _is_plan_approval_message(user_message: str) -> bool:
    lowered = (user_message or "").lower()
    if any(keyword in lowered for keyword in PLAN_APPROVAL_KEYWORDS):
        return True
    return bool(re.search(r"\b(approve|approved|proceed|continue)\b", lowered) and "plan" in lowered)


def _resolve_enable_thinking_for_chat(reasoning_mode: str | None) -> bool:
    normalized = (reasoning_mode or "").strip().lower()
    return normalized == "reasoning"


def _extract_write_filename(tool_input: dict[str, Any]) -> str:
    filename = tool_input.get("filename") or tool_input.get("name")
    if isinstance(filename, str) and filename.strip():
        return filename.strip()
    path_like = tool_input.get("path") or tool_input.get("file_path") or tool_input.get("filepath") or ""
    if isinstance(path_like, str) and path_like.strip():
        return Path(path_like.replace("file://", "").strip()).name
    return ""


def _build_project_governance_block(
    *,
    project_mode: bool,
    plan_required: bool,
    approval_mode: str,
    plan_status: str,
) -> str:
    if not project_mode:
        return ""

    lines = [
        "## Project Build Governance",
        "- Project mode is active for this session.",
        "- Always work in phases and emit phase reports (PHASE_N_REPORT.md).",
        "- Before implementation, produce BUILD_PLAN.md with milestones, risks, and test strategy.",
        "- Use session workspace tools first: pwd, ls, mkdir -p, write files, run tests, patch, repeat.",
    ]
    if not plan_required:
        lines.append("- Plan approval gate is disabled by policy; proceed after writing BUILD_PLAN.md.")
        return "\n".join(lines)

    if approval_mode == "auto":
        lines.append("- Approval mode: auto. Build plan must still be written, then proceed without waiting.")
    else:
        if plan_status != "approved":
            lines.append("- Approval mode: manual.")
            lines.append("- Stop after drafting BUILD_PLAN.md and request explicit user approval (e.g., 'approve plan').")
            lines.append("- Do not create implementation code files until plan is approved.")
        else:
            lines.append("- Plan is approved. Continue implementation phase-by-phase.")

    return "\n".join(lines)


def _clean_result_blob(tool_result: str) -> str:
    cleaned = tool_result.strip()
    if not cleaned:
        return ""

    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _parse_result_payload(tool_result: str) -> Any | None:
    cleaned = _clean_result_blob(tool_result)
    if not cleaned:
        return None

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # MCP-backed tools occasionally return Python-literal-ish payloads.
    try:
        parsed = ast.literal_eval(cleaned)
        if isinstance(parsed, (dict, list)):
            return parsed
    except Exception:
        return None
    return None


def _looks_like_write_tool(tool_name: str) -> bool:
    name = (tool_name or "").strip().lower()
    if not name:
        return False
    return (
        name == "write_file"
        or name.endswith(".write_file")
        or name.endswith("/write_file")
        or name.endswith(":write_file")
        or "__write_file" in name
        or "write_file" in name
    )


def _extract_path_like(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    candidate = value.strip()
    if not candidate:
        return None
    if "/" in candidate or "\\" in candidate or candidate.startswith("file://"):
        return candidate
    return None


def _write_file_missing_args_error(result: str) -> bool:
    text = (result or "").lower()
    if "write_file requires both" in text:
        return True
    if "executing tool 'write_file'" in text and "'filename'" in text:
        return True
    if "executing tool 'write_file'" in text and "'content'" in text:
        return True
    return False


def _build_write_file_retry_input(
    tool_input: dict[str, Any],
    assistant_content_dicts: list[dict[str, Any]],
    session_id: str,
) -> dict[str, str] | None:
    merged = dict(tool_input or {})
    raw_args = merged.get("_raw_arguments")
    if isinstance(raw_args, str) and raw_args.strip():
        try:
            parsed = json.loads(raw_args)
            if isinstance(parsed, dict):
                merged = {**parsed, **merged}
        except Exception:
            pass

    filename = merged.get("filename") or merged.get("name")
    path_like = merged.get("path") or merged.get("file_path") or merged.get("filepath") or merged.get("uri")
    if (not filename) and isinstance(path_like, str) and path_like.strip():
        cleaned = path_like.replace("file://", "").strip()
        filename = Path(cleaned).name

    content = (
        merged.get("content")
        or merged.get("text")
        or merged.get("body")
        or merged.get("contents")
        or merged.get("data")
    )

    if content is None:
        text_blocks = []
        for block in assistant_content_dicts:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text" and isinstance(block.get("text"), str):
                text_blocks.append(block["text"])
        stitched = "\n\n".join(part for part in text_blocks if part.strip())
        if stitched.strip():
            content = stitched

    if isinstance(content, (dict, list)):
        content = json.dumps(content, ensure_ascii=False, indent=2)
    if content is not None and not isinstance(content, str):
        content = str(content)

    if not isinstance(filename, str) or not filename.strip():
        filename = f"artifact_{session_id[:8]}_{int(time.time())}.md"

    if not isinstance(content, str) or not content.strip():
        return None

    return {"filename": filename.strip(), "content": content}


async def _extract_artifact_info(
    *,
    tool_name: str,
    tool_input: dict[str, Any],
    tool_result: str,
    session_id: str,
) -> dict[str, Any] | None:
    """Parse artifact info from tool output.

    Supports:
    - native `write_file` JSON output (already has file_id),
    - MCP filesystem-style outputs with path/filename metadata.
    """
    payload = _parse_result_payload(tool_result)
    if isinstance(payload, dict):
        # Handle wrappers like {"result": {...}} or {"data": {...}}.
        for key in ("result", "data", "output", "file"):
            nested = payload.get(key)
            if isinstance(nested, dict) and (
                nested.get("file_id") or nested.get("path") or nested.get("filename")
            ):
                payload = nested
                break

        if payload.get("file_id") and payload.get("filename"):
            return payload

    if not _looks_like_write_tool(tool_name):
        return None

    source_path = None
    filename = None

    if isinstance(payload, dict):
        source_path = (
            _extract_path_like(payload.get("path"))
            or _extract_path_like(payload.get("file_path"))
            or _extract_path_like(payload.get("filepath"))
            or _extract_path_like(payload.get("uri"))
        )
        for key in ("filename", "name", "basename"):
            raw = payload.get(key)
            if isinstance(raw, str) and raw.strip():
                filename = raw.strip()
                break

    if not source_path:
        source_path = (
            _extract_path_like(tool_input.get("path"))
            or _extract_path_like(tool_input.get("file_path"))
            or _extract_path_like(tool_input.get("filepath"))
            or _extract_path_like(tool_input.get("uri"))
        )
    if not filename:
        raw_name = tool_input.get("filename") or tool_input.get("name")
        if isinstance(raw_name, str) and raw_name.strip():
            filename = raw_name.strip()

    if source_path:
        imported = await file_ops.import_external_artifact(
            session_id=session_id,
            source_path=source_path,
            filename=filename,
        )
        if imported and imported.get("file_id") and imported.get("filename"):
            return imported

    # Final fallback: if tool passed filename+content but output is unstructured,
    # mirror into session uploads so UI still gets deterministic artifact events.
    if filename and isinstance(tool_input.get("content"), str):
        try:
            mirrored = await file_ops.write_file(
                filename=filename,
                content=tool_input["content"],
                session_id=session_id,
            )
            mirrored_payload = _parse_result_payload(mirrored)
            if isinstance(mirrored_payload, dict) and mirrored_payload.get("file_id"):
                mirrored_payload["source"] = "mcp"
                mirrored_payload["source_path"] = source_path
                return mirrored_payload
        except Exception:
            return None

    return None


def _truncate_for_context(value: Any, max_chars: int) -> str:
    text = str(value or "")
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n...[truncated {len(text) - max_chars} chars]"


def _convert_content_for_api(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert stored messages to API-compatible format."""
    converted: list[dict[str, Any]] = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")

        if role == "system":
            continue

        if isinstance(content, list):
            converted_content: list[dict[str, Any]] = []
            for block in content:
                if hasattr(block, "__dict__"):
                    block = block.__dict__

                if isinstance(block, dict):
                    block_type = block.get("type")
                    if block_type == "text":
                        converted_content.append(
                            {
                                "type": "text",
                                "text": _truncate_for_context(
                                    block.get("text", ""),
                                    MAX_TEXT_BLOCK_CHARS_FOR_CONTEXT,
                                ),
                            }
                        )
                    elif block_type == "thinking":
                        if INCLUDE_THINKING_IN_CONTEXT:
                            converted_content.append(
                                {
                                    "type": "text",
                                    "text": _truncate_for_context(
                                        block.get("thinking", ""),
                                        MAX_TEXT_BLOCK_CHARS_FOR_CONTEXT,
                                    ),
                                }
                            )
                    elif block_type == "tool_result":
                        converted_content.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.get("tool_use_id") or block.get("tool_id") or "",
                                "content": _truncate_for_context(
                                    block.get("content") or block.get("result") or "",
                                    MAX_TOOL_RESULT_CHARS_FOR_CONTEXT,
                                ),
                            }
                        )
                    else:
                        converted_content.append(block)
                else:
                    converted_content.append({"type": "text", "text": _truncate_for_context(block, MAX_TEXT_BLOCK_CHARS_FOR_CONTEXT)})

            converted.append({"role": role, "content": converted_content})
            continue

        converted.append(
            {
                "role": role,
                "content": [
                    {
                        "type": "text",
                        "text": _truncate_for_context(content, MAX_TEXT_BLOCK_CHARS_FOR_CONTEXT),
                    }
                ],
            }
        )

    return converted


def _sanitize_audio_block_for_persistence(block: dict[str, Any]) -> dict[str, Any]:
    block_type = block.get("type")
    if block_type == "input_audio":
        input_audio = block.get("input_audio") if isinstance(block.get("input_audio"), dict) else {}
        return {
            "type": "input_audio",
            "filename": block.get("filename") or input_audio.get("filename") or "voice input",
            "mime_type": block.get("mime_type") or input_audio.get("mime_type") or "audio/wav",
            "duration_ms": block.get("duration_ms"),
            "input_audio": {
                "format": input_audio.get("format") or "wav",
            },
        }
    if block_type == "audio_url":
        audio_url = block.get("audio_url") if isinstance(block.get("audio_url"), dict) else {}
        return {
            "type": "audio_url",
            "filename": block.get("filename") or audio_url.get("filename") or "voice input",
            "mime_type": block.get("mime_type") or audio_url.get("mime_type") or "audio/webm",
            "duration_ms": block.get("duration_ms"),
            "audio_url": {
                "url": "",
            },
        }
    return block


def _sanitize_messages_for_persistence(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    for msg in messages:
        content = msg.get("content")
        if not isinstance(content, list):
            sanitized.append(msg)
            continue
        next_content: list[dict[str, Any]] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") in {"input_audio", "audio_url"}:
                next_content.append(_sanitize_audio_block_for_persistence(block))
            else:
                next_content.append(block)
        sanitized.append({**msg, "content": next_content})
    return sanitized


def _serialize_content_blocks(blocks: list[Any]) -> list[dict[str, Any]]:
    serialized: list[dict[str, Any]] = []
    for block in blocks:
        block_type = getattr(block, "type", None) or (block.get("type") if isinstance(block, dict) else "text")

        if block_type == "thinking":
            thinking_text = getattr(block, "thinking", None)
            if thinking_text is None and isinstance(block, dict):
                thinking_text = block.get("thinking")
            serialized.append({"type": "thinking", "thinking": thinking_text or ""})
        elif block_type == "tool_use":
            serialized.append(
                {
                    "type": "tool_use",
                    "tool_id": getattr(block, "id", None) or (block.get("id") if isinstance(block, dict) else ""),
                    "tool_name": getattr(block, "name", None) or (block.get("name") if isinstance(block, dict) else ""),
                    "input": getattr(block, "input", None) or (block.get("input") if isinstance(block, dict) else {}),
                }
            )
        else:
            text = getattr(block, "text", None)
            if text is None and isinstance(block, dict):
                text = block.get("text")
            serialized.append({"type": "text", "text": text or ""})

    return serialized


def _extract_text(content_dicts: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for block in content_dicts:
        if block.get("type") == "text":
            parts.append(str(block.get("text") or ""))
    return "\n".join(part for part in parts if part).strip()


def _should_enforce_verification(user_message: str, tools_used: set[str]) -> bool:
    if not STRICT_VERIFICATION_MODE:
        return False

    lowered = user_message.lower()
    if any(keyword in lowered for keyword in VERIFY_KEYWORDS):
        return True

    return "web_search" in tools_used


def _apply_verification_guard(
    user_message: str,
    content_dicts: list[dict[str, Any]],
    tools_used: set[str],
) -> tuple[list[dict[str, Any]], bool]:
    if not _should_enforce_verification(user_message, tools_used):
        return content_dicts, False

    combined_text = _extract_text(content_dicts)
    has_source_citation = bool(re.search(r"https?://", combined_text))

    if has_source_citation:
        return content_dicts, False

    note = (
        "\n\nVerification note: This answer does not yet include explicit evidence links. "
        "Treat it as provisional and run verification (for example via web_search) before relying on factual claims."
    )

    patched = [*content_dicts, {"type": "text", "text": note}]
    return patched, True


async def run_agent(
    session_id: str,
    user_message: str,
    file_ids: list[str],
    stream_callback: Callable[[dict], Any],
    *,
    reasoning_mode: str | None = None,
    audio_input: dict[str, Any] | None = None,
    audio_url: dict[str, Any] | None = None,
    provider_override: BaseLLMProvider | None = None,
) -> None:
    """Run the autonomous tool loop for a session."""

    memory = await get_memory_service()
    multimodal_provider = get_multimodal_audio_provider() if (audio_input or audio_url) else None
    if (audio_input or audio_url) and multimodal_provider is None:
        await stream_callback(
            {
                "type": "error",
                "message": (
                    "Direct audio input is enabled for this turn, but no multimodal audio provider "
                    "is configured. Set DIRECT_AUDIO_* or PHI_4_INSTRUCT_* env vars."
                ),
            }
        )
        return
    provider = provider_override or multimodal_provider or get_provider()
    replay = SessionReplayLogger(session_id=session_id, enabled=ENABLE_REPLAY_LOGS)

    await replay.log(
        "session_start",
        {
            "session_id": session_id,
            "provider": provider.provider_name,
            "model": provider.model_name,
            "fallbacks": getattr(provider, "fallbacks", []),
            "max_iterations": MAX_ITERATIONS,
            "direct_audio": bool(audio_input or audio_url),
        },
    )

    await memory.start_session(session_id)
    messages = await memory.get_messages(session_id)
    session_state = await memory.get_session_state(session_id)
    await memory.maybe_capture_user_profile(user_message)
    user_profile = await memory.get_user_profile()
    now_utc = datetime.now(timezone.utc)
    temporal_context = _build_temporal_context_block(
        session_state=session_state,
        user_timezone=str(user_profile.get("timezone") or ""),
        now_utc=now_utc,
    )
    project_mode = _is_project_build_request(user_message) or bool(session_state.get("build_plan_required") == "true")
    plan_required = _env_bool("AGENT_REQUIRE_PLAN_FOR_PROJECTS", True)
    approval_mode = "auto" if os.getenv("AGENT_PLAN_APPROVAL_MODE", "manual").strip().lower() in {"auto", "always"} else "manual"
    plan_status = str(session_state.get("build_plan_status") or "none").lower()

    if project_mode and plan_required:
        approval_msg = _is_plan_approval_message(user_message)
        if approval_mode == "auto" and plan_status in {"pending"}:
            plan_status = "approved"
        elif approval_msg and plan_status in {"pending"}:
            plan_status = "approved"
        await memory.update_session_state(
            session_id,
            {
                "build_plan_required": True,
                "build_plan_auto_approve": approval_mode == "auto",
                "build_plan_status": plan_status,
                "build_plan_requested_at": int(time.time()),
            },
        )
        session_state = await memory.get_session_state(session_id)
        plan_status = str(session_state.get("build_plan_status") or "none").lower()

    if not str(session_state.get("goal") or "").strip():
        await memory.update_session_state(
            session_id,
            {
                "goal": user_message,
                "status": "running",
                "next_step": "Plan and execute the next best action.",
                "last_user_message_at": now_utc.isoformat(),
                "last_agent_run_at": now_utc.isoformat(),
            },
        )
    else:
        await memory.update_session_state(
            session_id,
            {
                "status": "running",
                "last_user_message_at": now_utc.isoformat(),
                "last_agent_run_at": now_utc.isoformat(),
            },
        )

    context = await memory.build_context(user_message)
    identity_context = await memory.build_identity_context_block(session_id, user_message)
    core_prompt = memory.get_core_prompt_block()
    agent_rules = _load_optional_text(AGENTS_RULES_PATH)
    project_governance = _build_project_governance_block(
        project_mode=project_mode,
        plan_required=plan_required,
        approval_mode=approval_mode,
        plan_status=plan_status,
    )

    system_prompt = _load_prompt("SYSTEM_PROMPT_PATH", "system_prompt.md", DEFAULT_SYSTEM_PROMPT)
    eval_prompt_text = _load_prompt("TOOL_EVALUATION_PROMPT_PATH", "tool_evaluation_prompt.md", DEFAULT_EVAL_PROMPT)
    base_system_prompt = temporal_context + "\n\n" + system_prompt
    if agent_rules:
        base_system_prompt += "\n\n" + agent_rules
    if identity_context:
        base_system_prompt += "\n\n" + identity_context
    if context:
        base_system_prompt += "\n\n" + context
    if project_governance:
        base_system_prompt += "\n\n" + project_governance
    base_system_prompt += "\n\n" + core_prompt

    skills_prompt, selected_skills = build_skills_prompt(user_message)
    if skills_prompt:
        base_system_prompt += "\n\n" + skills_prompt
        for skill in selected_skills:
            await stream_callback(
                {
                    "type": "skill",
                    "skill_name": skill.name,
                    "skill_file": str(skill.file_path),
                    "skill_reason": skill.reason,
                    "skill_score": skill.score,
                }
            )
        await replay.log(
            "skills_selected",
            {
                "skills": [
                    {
                        "name": s.name,
                        "file": str(s.file_path),
                        "reason": s.reason,
                        "score": s.score,
                    }
                    for s in selected_skills
                ]
            },
        )

    user_content: list[dict[str, Any]] = []
    if user_message:
        user_content.append({"type": "text", "text": user_message})

    if file_ids:
        include_images = bool(getattr(provider, "supports_image_prompt_blocks", False))
        for file_id in file_ids:
            blocks = await file_ops.get_file_prompt_blocks(file_id, include_images=include_images)
            user_content.extend(blocks)

    if isinstance(audio_input, dict) and str(audio_input.get("data") or "").strip():
        user_content.append(
            {
                "type": "input_audio",
                "filename": audio_input.get("filename") or "recording.wav",
                "mime_type": audio_input.get("mime_type") or "audio/wav",
                "duration_ms": audio_input.get("duration_ms"),
                "input_audio": {
                    "data": str(audio_input.get("data") or ""),
                    "format": str(audio_input.get("format") or "wav"),
                    "filename": audio_input.get("filename"),
                    "mime_type": audio_input.get("mime_type"),
                },
            }
        )
    elif isinstance(audio_url, dict) and str(audio_url.get("url") or "").strip():
        user_content.append(
            {
                "type": "audio_url",
                "filename": audio_url.get("filename") or "voice-input",
                "mime_type": audio_url.get("mime_type") or "audio/webm",
                "duration_ms": audio_url.get("duration_ms"),
                "audio_url": {
                    "url": str(audio_url.get("url") or ""),
                    "filename": audio_url.get("filename"),
                    "mime_type": audio_url.get("mime_type"),
                },
            }
        )

    messages.append({"role": "user", "content": user_content})
    await memory.save_messages(session_id, _sanitize_messages_for_persistence(messages))

    iteration = 0
    total_input_tokens = 0
    total_output_tokens = 0
    peak_input_tokens = 0
    total_tool_calls = 0
    tools_used: set[str] = set()
    reported_context_window = _resolve_effective_context_window(provider, AGENT_MAX_TOKENS)

    while iteration < MAX_ITERATIONS:
        iteration += 1

        iteration_state = await memory.get_session_state(session_id)
        loaded_tool_names = list(iteration_state.get("loaded_tool_schemas", []))
        active_tool_definitions = _select_tool_definitions(
            loaded_tool_names=loaded_tool_names,
        )
        iteration_system_prompt = base_system_prompt + "\n\n" + build_tools_prompt_block(
            TOOL_DEFINITIONS,
            loaded_tool_names=loaded_tool_names,
        )
        if INCLUDE_HARNESS_METADATA_IN_PROMPT:
            harness_metadata = await _build_harness_metadata_block(active_tool_definitions)
            iteration_system_prompt += "\n\n" + harness_metadata

        history_char_budget, reported_context_window = _history_char_budget_for_iteration(
            provider=provider,
            system_prompt=iteration_system_prompt,
            requested_max_tokens=AGENT_MAX_TOKENS,
        )
        if hasattr(memory, "prepare_messages_for_model"):
            messages_for_model = await memory.prepare_messages_for_model(
                messages,
                max_chars=history_char_budget,
            )
        else:
            messages_for_model = messages
        api_messages = _convert_content_for_api(messages_for_model)

        await replay.log(
            "iteration_start",
            {
                "iteration": iteration,
                "message_count": len(api_messages),
                "tool_count": len(active_tool_definitions),
                "tools": [tool.get("name") for tool in active_tool_definitions],
                "loaded_tool_schemas": loaded_tool_names,
                "history_char_budget": history_char_budget,
                "context_window": reported_context_window,
            },
        )

        try:
            streamed_text = False
            streamed_thinking = False
            emitted_stream_tool_ids: set[str] = set()

            async def provider_stream_event(block: LLMContentBlock) -> None:
                nonlocal streamed_text, streamed_thinking
                if block.type == "thinking":
                    streamed_thinking = True
                    await stream_callback({"type": "thinking", "block_index": 0, "text": block.thinking or ""})
                    return
                if block.type == "text":
                    streamed_text = True
                    await stream_callback({"type": "text", "text": block.text or ""})
                    return
                if block.type == "tool_use":
                    tool_id = block.id or ""
                    if tool_id and tool_id in emitted_stream_tool_ids:
                        return
                    if tool_id:
                        emitted_stream_tool_ids.add(tool_id)
                    await stream_callback(
                        {
                            "type": "tool_call",
                            "tool_name": block.name or "",
                            "tool_id": tool_id,
                            "input": block.input or {},
                        }
                    )

            response = await provider.generate(
                system=iteration_system_prompt,
                tools=active_tool_definitions,
                messages=api_messages,
                max_tokens=AGENT_MAX_TOKENS,
                temperature=AGENT_TEMPERATURE,
                enable_thinking=_resolve_enable_thinking_for_chat(reasoning_mode),
                on_stream_event=provider_stream_event,
            )
            response_provider = response.provider_name or provider.provider_name
            response_model = response.model_name or provider.model_name

            input_tokens = int(response.usage.input_tokens)
            output_tokens = int(response.usage.output_tokens)
            total_input_tokens += input_tokens
            total_output_tokens += output_tokens
            peak_input_tokens = max(peak_input_tokens, input_tokens)

            await memory.record_tokens(input_tokens, output_tokens)
            await replay.log(
                "iteration_response",
                {
                    "iteration": iteration,
                    "stop_reason": response.stop_reason,
                    "provider": response_provider,
                    "model": response_model,
                    "fallback_used": response.fallback_used,
                    "notice": response.notice,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "blocks": [b.type for b in response.content],
                },
            )

            for i, block in enumerate(response.content):
                if block.type == "thinking":
                    if not streamed_thinking:
                        await stream_callback({"type": "thinking", "block_index": i, "text": block.thinking or ""})
                elif block.type == "text":
                    if not streamed_text:
                        await stream_callback({"type": "text", "text": block.text or ""})
                elif block.type == "tool_use":
                    if block.id and block.id in emitted_stream_tool_ids:
                        continue
                    await stream_callback(
                        {
                            "type": "tool_call",
                            "tool_name": block.name,
                            "tool_id": block.id,
                            "input": block.input or {},
                        }
                    )

            content_dicts = _serialize_content_blocks(response.content)
            if response.notice and response.stop_reason == "end_turn":
                content_dicts.append({"type": "text", "text": f"\n\n{response.notice}"})

            if response.stop_reason == "end_turn":
                content_dicts, verification_flagged = _apply_verification_guard(
                    user_message=user_message,
                    content_dicts=content_dicts,
                    tools_used=tools_used,
                )

                if verification_flagged:
                    await stream_callback(
                        {
                            "type": "text",
                            "text": "\n\nVerification note: missing explicit source links; answer marked provisional.",
                        }
                    )

                messages.append({"role": "assistant", "content": content_dicts})
                await memory.save_messages(session_id, _sanitize_messages_for_persistence(messages))
                summary = _extract_text(content_dicts)[:1000]
                latest_state = await memory.get_session_state(session_id)
                state_update: dict[str, Any] = {
                    "status": "idle",
                    "last_summary": summary,
                    "next_step": "Await next user directive or continue follow-up requested by user.",
                    "done_count": int(latest_state.get("done_count", 0)) + 1,
                }
                if project_mode and plan_required and approval_mode == "manual":
                    if str(latest_state.get("build_plan_status") or "none").lower() != "approved":
                        state_update["build_plan_status"] = "pending"
                        state_update["build_plan_summary"] = summary
                        state_update["next_step"] = "Await explicit user plan approval before implementation."
                await memory.update_session_state(session_id, state_update)

                await stream_callback(
                    {
                        "type": "done",
                        "total_input_tokens": total_input_tokens,
                        "total_output_tokens": total_output_tokens,
                        "iterations": iteration,
                        "max_iterations": MAX_ITERATIONS,
                        "context_input_tokens": peak_input_tokens,
                        "context_window": reported_context_window,
                        "provider": response_provider,
                        "model": response_model,
                        "fallback_used": response.fallback_used,
                        "provider_notice": response.notice,
                        "tool_calls": total_tool_calls,
                        "replay_path": replay.metadata().get("path"),
                    }
                )

                await replay.log(
                    "session_done",
                    {
                        "iterations": iteration,
                        "total_input_tokens": total_input_tokens,
                        "total_output_tokens": total_output_tokens,
                        "total_tool_calls": total_tool_calls,
                    },
                )

                await memory.end_session()
                return

            if response.stop_reason == "tool_use":
                tool_blocks = [block for block in response.content if block.type == "tool_use"]

                if not tool_blocks:
                    await stream_callback({"type": "error", "message": "Model requested tool_use without tool blocks"})
                    await memory.end_session()
                    return

                remaining_budget = max(0, MAX_TOOL_CALLS_PER_RUN - total_tool_calls)
                allowed_calls = min(len(tool_blocks), MAX_TOOL_CALLS_PER_ITERATION, remaining_budget)

                if allowed_calls < len(tool_blocks):
                    await stream_callback(
                        {
                            "type": "text",
                            "text": (
                                f"\n\nTool governance: executed {allowed_calls}/{len(tool_blocks)} tool calls "
                                f"(iteration cap {MAX_TOOL_CALLS_PER_ITERATION}, run budget left {remaining_budget})."
                            ),
                        }
                    )

                tool_results: list[dict[str, Any]] = []
                iteration_tools: list[str] = []
                plan_artifact_written = False

                for idx, block in enumerate(tool_blocks):
                    tool_id = block.id or f"tool_{iteration}_{idx}"
                    tool_name = block.name or ""
                    tool_input = block.input or {}

                    await stream_callback(
                        {
                            "type": "tool_call",
                            "tool_name": tool_name,
                            "tool_id": tool_id,
                            "input": tool_input,
                        }
                    )

                    if idx >= allowed_calls:
                        result = "Error: Tool call skipped by governance limits. Continue in next iteration if required."
                    else:
                        plan_status = str((await memory.get_session_state(session_id)).get("build_plan_status") or "none").lower()
                        if project_mode and plan_required and approval_mode == "manual" and plan_status != "approved":
                            if tool_name == "write_file":
                                target_name = _extract_write_filename(tool_input).lower()
                                if target_name == "build_plan.md":
                                    result = await dispatch_tool(tool_name, tool_input, session_id)
                                    total_tool_calls += 1
                                    tools_used.add(tool_name)
                                    iteration_tools.append(tool_name)
                                else:
                                    result = (
                                        "Error: Plan approval required. Only BUILD_PLAN.md may be written before approval. "
                                        "Ask user to approve plan explicitly."
                                    )
                            elif tool_name in {
                                "list_files",
                                "read_file",
                                "web_search",
                                "search_web",
                                "tavily_search",
                                "brave_search",
                                "scrape_page",
                                "extract_contacts",
                                "list_leads",
                                "run_campaign",
                                "summarize_document",
                                "calculate",
                                "run_workspace_diagnostics",
                            }:
                                result = await dispatch_tool(tool_name, tool_input, session_id)
                                total_tool_calls += 1
                                tools_used.add(tool_name)
                                iteration_tools.append(tool_name)
                            else:
                                result = (
                                    "Error: Plan approval required before implementation commands. "
                                    "Draft BUILD_PLAN.md and wait for user approval."
                                )
                        else:
                            result = await dispatch_tool(tool_name, tool_input, session_id)
                            total_tool_calls += 1
                            tools_used.add(tool_name)
                            iteration_tools.append(tool_name)

                        if (
                            _looks_like_write_tool(tool_name)
                            and _write_file_missing_args_error(str(result))
                        ):
                            retry_input = _build_write_file_retry_input(
                                tool_input=tool_input,
                                assistant_content_dicts=content_dicts,
                                session_id=session_id,
                            )
                            if retry_input:
                                repaired = await dispatch_tool("write_file", retry_input, session_id)
                                if not str(repaired).startswith("Error"):
                                    await replay.log(
                                        "tool_auto_repair",
                                        {
                                            "iteration": iteration,
                                            "tool_id": tool_id,
                                            "tool_name": tool_name,
                                            "original_error": str(result)[:400],
                                            "retry_input_keys": sorted(retry_input.keys()),
                                        },
                                    )
                                    result = repaired

                    await replay.log(
                        "tool_result",
                        {
                            "iteration": iteration,
                            "tool_id": tool_id,
                            "tool_name": tool_name,
                            "input": tool_input,
                            "result_preview": str(result)[:600],
                        },
                    )

                    await stream_callback({"type": "tool_result", "tool_id": tool_id, "result": result})

                    file_info = await _extract_artifact_info(
                        tool_name=tool_name,
                        tool_input=tool_input,
                        tool_result=result,
                        session_id=session_id,
                    )
                    if file_info and file_info.get("file_id") and file_info.get("filename"):
                        if str(file_info.get("filename", "")).lower() == "build_plan.md":
                            plan_artifact_written = True
                        await stream_callback(
                            {
                                "type": "artifact",
                                "file_id": file_info.get("file_id"),
                                "filename": file_info.get("filename"),
                                "size": file_info.get("size"),
                                "path": file_info.get("path"),
                                "timestamp": file_info.get("timestamp"),
                                "validation": file_info.get("validation"),
                                "source": file_info.get("source"),
                                "source_path": file_info.get("source_path"),
                            }
                        )

                    tool_results.append({"type": "tool_result", "tool_use_id": tool_id, "content": result})

                messages.append({"role": "assistant", "content": content_dicts})
                messages.append({"role": "user", "content": tool_results})
                messages.append({"role": "user", "content": eval_prompt_text})
                await memory.save_messages(session_id, _sanitize_messages_for_persistence(messages))
                await memory.register_tools_for_session(session_id, iteration_tools)
                await memory.update_session_state(
                    session_id,
                    {
                        "status": "running",
                        "next_step": "Evaluate latest tool outputs and decide whether to continue, revise, switch tools, or conclude.",
                        "last_summary": _extract_text(content_dicts)[:700],
                    },
                )
                if project_mode and plan_required and plan_artifact_written:
                    if approval_mode == "auto":
                        await memory.update_session_state(
                            session_id,
                            {
                                "build_plan_status": "approved",
                                "next_step": "Plan auto-approved by policy. Begin implementation phase.",
                            },
                        )
                    else:
                        await memory.update_session_state(
                            session_id,
                            {
                                "build_plan_status": "pending",
                                "next_step": "Await explicit user approval for BUILD_PLAN.md before implementation.",
                            },
                        )

                continue

            # Unknown stop reason
            await stream_callback(
                {
                    "type": "done",
                    "total_input_tokens": total_input_tokens,
                    "total_output_tokens": total_output_tokens,
                    "iterations": iteration,
                    "max_iterations": MAX_ITERATIONS,
                    "context_input_tokens": peak_input_tokens,
                    "context_window": reported_context_window,
                    "provider": provider.provider_name,
                    "model": provider.model_name,
                    "tool_calls": total_tool_calls,
                    "replay_path": replay.metadata().get("path"),
                }
            )
            await memory.update_session_state(
                session_id,
                {
                    "status": "idle",
                    "next_step": "Unknown stop reason encountered; validate model response and continue as needed.",
                },
            )
            await memory.end_session()
            return

        except Exception as e:
            print(f"[Agent] Iteration {iteration} failed: {e}")
            traceback.print_exc()
            await replay.log("session_error", {"iteration": iteration, "error": str(e)})
            await stream_callback({"type": "error", "message": str(e)})
            await memory.update_session_state(
                session_id,
                {"status": "error", "next_step": f"Recover from error: {str(e)[:240]}"},
            )
            try:
                await memory.end_session()
            except Exception:
                pass
            return

    await stream_callback({"type": "error", "message": f"Max iterations ({MAX_ITERATIONS}) reached"})
    await memory.update_session_state(
        session_id,
        {
            "status": "paused",
            "next_step": "Max iterations reached; request user continuation to proceed.",
        },
    )

    try:
        await memory.end_session()
    except Exception:
        pass
