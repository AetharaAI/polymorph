from __future__ import annotations

from typing import Any

from backend.agent.runner import run_agent

from .base import ChannelInboundMessage


def _extract_text(event: dict[str, Any]) -> str:
    return str(event.get("text") or "").strip()


async def run_channel_turn(message: ChannelInboundMessage) -> dict[str, Any]:
    text_chunks: list[str] = []
    errors: list[str] = []
    tool_calls: list[dict[str, Any]] = []
    usage: dict[str, Any] = {}

    async def stream_callback(event: dict[str, Any]) -> None:
        event_type = str(event.get("type") or "")
        if event_type == "text":
            chunk = _extract_text(event)
            if chunk:
                text_chunks.append(chunk)
        elif event_type == "tool_call":
            tool_calls.append(
                {
                    "tool_name": str(event.get("tool_name") or ""),
                    "tool_id": str(event.get("tool_id") or ""),
                }
            )
        elif event_type == "done":
            usage.update(event)
        elif event_type == "error":
            error_message = str(event.get("message") or "").strip()
            if error_message:
                errors.append(error_message)

    await run_agent(
        session_id=message.session_id,
        user_message=message.text,
        file_ids=[],
        stream_callback=stream_callback,
    )

    assistant_text = "\n".join(chunk for chunk in text_chunks if chunk).strip()
    return {
        "status": "error" if errors else "ok",
        "assistant_text": assistant_text,
        "errors": errors,
        "tool_calls": tool_calls,
        "usage": usage,
    }
