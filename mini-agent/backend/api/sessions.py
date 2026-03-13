from __future__ import annotations

import ast
import json
import re
import time
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from backend.agent.tools import file_ops
from backend.memory import get_memory_service

router = APIRouter()


def _clean_payload_blob(raw: str) -> str:
    cleaned = (raw or "").strip()
    if not cleaned:
        return ""
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _parse_payload(raw: str) -> Any | None:
    cleaned = _clean_payload_blob(raw)
    if not cleaned:
        return None
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    try:
        parsed = ast.literal_eval(cleaned)
        if isinstance(parsed, (dict, list)):
            return parsed
    except Exception:
        return None
    return None


def _extract_artifact(result_text: str) -> dict[str, Any] | None:
    payload = _parse_payload(result_text)
    if not isinstance(payload, dict):
        return None
    if not payload.get("file_id") or not payload.get("filename"):
        return None
    return {
        "file_id": str(payload.get("file_id")),
        "filename": str(payload.get("filename")),
        "size": int(payload.get("size") or 0),
        "path": str(payload.get("path") or ""),
        "timestamp": int(payload.get("timestamp") or int(time.time() * 1000)),
        "validation": payload.get("validation"),
        "source": payload.get("source"),
        "source_path": payload.get("source_path"),
    }


def _looks_like_eval_prompt(text: str) -> bool:
    normalized = text.strip()
    return normalized.startswith("## Tool Execution Complete") or "Evaluate the tool results" in normalized


def _extract_user_visible_text(blocks: list[dict[str, Any]]) -> str:
    text_blocks = [
        str(block.get("text", "")).strip()
        for block in blocks
        if isinstance(block, dict) and block.get("type") == "text"
    ]
    if not text_blocks:
        return ""

    filtered = [
        t for t in text_blocks
        if t
        and not t.startswith("[File content from ")
        and not t.startswith("[Image attachment: ")
        and not _looks_like_eval_prompt(t)
    ]
    source = filtered if filtered else text_blocks
    return source[-1] if source else ""


def _normalize_messages_for_ui(messages: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ui_messages: list[dict[str, Any]] = []
    artifacts_by_id: dict[str, dict[str, Any]] = {}
    base_ts = int(time.time() * 1000)

    for idx, msg in enumerate(messages):
        role = str(msg.get("role") or "")
        if role == "system":
            continue

        content = msg.get("content")
        if isinstance(content, str):
            content_blocks = [{"type": "text", "text": content}]
        elif isinstance(content, list):
            content_blocks = [b for b in content if isinstance(b, dict)]
        else:
            content_blocks = [{"type": "text", "text": str(content or "")}]

        ts = base_ts + idx

        if role == "assistant":
            normalized_blocks: list[dict[str, Any]] = []
            for block in content_blocks:
                block_type = block.get("type")
                if block_type == "text":
                    text = str(block.get("text") or "")
                    if text:
                        normalized_blocks.append({"type": "text", "text": text})
                elif block_type == "thinking":
                    normalized_blocks.append({"type": "thinking", "thinking": str(block.get("thinking") or "")})
                elif block_type == "tool_use":
                    normalized_blocks.append(
                        {
                            "type": "tool_use",
                            "tool_name": str(block.get("tool_name") or block.get("name") or ""),
                            "tool_id": str(block.get("tool_id") or block.get("id") or ""),
                            "input": block.get("input") if isinstance(block.get("input"), dict) else {},
                        }
                    )
                elif block_type == "skill":
                    normalized_blocks.append(block)

            if normalized_blocks:
                ui_messages.append(
                    {
                        "id": f"{role}-{idx}",
                        "role": "assistant",
                        "timestamp": ts,
                        "content": normalized_blocks,
                    }
                )
            continue

        if role == "user":
            tool_result_blocks = [b for b in content_blocks if b.get("type") == "tool_result"]
            non_tool_blocks = [b for b in content_blocks if b.get("type") != "tool_result"]

            # Internal tool result turns get merged into previous assistant message.
            if tool_result_blocks and not non_tool_blocks:
                if not ui_messages or ui_messages[-1].get("role") != "assistant":
                    continue
                assistant_blocks = ui_messages[-1].setdefault("content", [])
                existing_tool_result_ids = {
                    str(b.get("tool_id"))
                    for b in assistant_blocks
                    if isinstance(b, dict) and b.get("type") == "tool_result"
                }
                for tr in tool_result_blocks:
                    tool_id = str(tr.get("tool_use_id") or tr.get("tool_id") or "")
                    result = str(tr.get("content") or tr.get("result") or "")
                    if tool_id in existing_tool_result_ids:
                        continue
                    assistant_blocks.append({"type": "tool_result", "tool_id": tool_id, "result": result})
                    artifact = _extract_artifact(result)
                    if artifact and artifact["file_id"] not in artifacts_by_id:
                        artifacts_by_id[artifact["file_id"]] = artifact
                continue

            visible_text = _extract_user_visible_text(content_blocks)
            if not visible_text:
                continue

            ui_messages.append(
                {
                    "id": f"{role}-{idx}",
                    "role": "user",
                    "timestamp": ts,
                    "content": [{"type": "text", "text": visible_text}],
                }
            )

    artifacts = sorted(artifacts_by_id.values(), key=lambda a: int(a.get("timestamp") or 0))
    return ui_messages, artifacts


@router.get("/sessions")
async def list_sessions(limit: int = Query(default=50, ge=1, le=500)):
    memory = await get_memory_service()
    sessions = await memory.list_sessions(limit=limit)
    return {"sessions": sessions}


@router.get("/sessions/{session_id}/state")
async def get_session_state(session_id: str):
    memory = await get_memory_service()
    messages = await memory.get_messages(session_id)
    if not isinstance(messages, list):
        raise HTTPException(status_code=404, detail="Session not found")

    ui_messages, artifacts = _normalize_messages_for_ui(messages)

    files_raw = await file_ops.list_files(session_id=session_id)
    try:
        files = json.loads(files_raw)
        if not isinstance(files, list):
            files = []
    except json.JSONDecodeError:
        files = []

    return {
        "session_id": session_id,
        "messages": ui_messages,
        "artifacts": artifacts,
        "files": files,
        "message_count": len(ui_messages),
    }
