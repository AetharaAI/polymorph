import json
import asyncio
import os
import sys
import time
from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.agent.runner import run_agent
from backend.models.schemas import ChatRequest

router = APIRouter()
SSE_EVENT_WAIT_TIMEOUT_SECONDS = float(os.getenv("SSE_EVENT_WAIT_TIMEOUT_SECONDS", "10"))
SSE_HEARTBEAT_SECONDS = float(os.getenv("SSE_HEARTBEAT_SECONDS", "10"))


async def event_generator(
    request: Request,
    session_id: str,
    message: str,
    file_ids: list[str],
    reasoning_mode: str | None,
    audio_input: dict | None,
    audio_url: dict | None,
):
    """Generate SSE events for the chat stream - yields immediately."""

    # Queue for passing events from callback to generator
    event_queue = asyncio.Queue()
    saw_terminal_event = False

    async def stream_callback(event: dict):
        """Callback that puts events into the queue."""
        nonlocal saw_terminal_event
        event_type = event.get("type")

        if event_type == "thinking":
            data = json.dumps({
                "block_index": event.get("block_index"),
                "text": event.get("text")
            })
            await event_queue.put(f"event: thinking\ndata: {data}\n\n")

        elif event_type == "text":
            data = json.dumps({"text": event.get("text")})
            await event_queue.put(f"event: text\ndata: {data}\n\n")

        elif event_type == "tool_call":
            data = json.dumps({
                "tool_name": event.get("tool_name"),
                "tool_id": event.get("tool_id"),
                "input": event.get("input")
            })
            await event_queue.put(f"event: tool_call\ndata: {data}\n\n")

        elif event_type == "tool_result":
            data = json.dumps({
                "tool_id": event.get("tool_id"),
                "result": event.get("result")
            })
            await event_queue.put(f"event: tool_result\ndata: {data}\n\n")

        elif event_type == "artifact":
            data = json.dumps({
                "file_id": event.get("file_id"),
                "filename": event.get("filename"),
                "size": event.get("size"),
                "path": event.get("path"),
                "timestamp": event.get("timestamp"),
                "validation": event.get("validation"),
                "source": event.get("source"),
                "source_path": event.get("source_path"),
            })
            await event_queue.put(f"event: artifact\ndata: {data}\n\n")

        elif event_type == "skill":
            data = json.dumps(
                {
                    "skill_name": event.get("skill_name"),
                    "skill_file": event.get("skill_file"),
                    "skill_reason": event.get("skill_reason"),
                    "skill_score": event.get("skill_score"),
                }
            )
            await event_queue.put(f"event: skill\ndata: {data}\n\n")

        elif event_type == "done":
            saw_terminal_event = True
            data = json.dumps({
                "total_input_tokens": event.get("total_input_tokens"),
                "total_output_tokens": event.get("total_output_tokens"),
                "iterations": event.get("iterations"),
                "max_iterations": event.get("max_iterations"),
                "context_input_tokens": event.get("context_input_tokens"),
                "context_window": event.get("context_window"),
                "provider": event.get("provider"),
                "model": event.get("model"),
                "tool_calls": event.get("tool_calls"),
                "replay_path": event.get("replay_path"),
            })
            await event_queue.put(f"event: done\ndata: {data}\n\n")

        elif event_type == "error":
            saw_terminal_event = True
            data = json.dumps({"message": event.get("message")})
            await event_queue.put(f"event: error\ndata: {data}\n\n")

    # Run the agent in a task
    agent_task = asyncio.create_task(
        run_agent(
            session_id,
            message,
            file_ids,
            stream_callback,
            reasoning_mode=reasoning_mode,
            audio_input=audio_input,
            audio_url=audio_url,
        )
    )
    last_heartbeat = time.monotonic()
    yield ": stream-open\n\n"

    # Yield events as they come in
    try:
        while True:
            if await request.is_disconnected():
                break
            try:
                event = await asyncio.wait_for(event_queue.get(), timeout=SSE_EVENT_WAIT_TIMEOUT_SECONDS)
                yield event
                last_heartbeat = time.monotonic()
            except asyncio.TimeoutError:
                # Check if agent is done
                if agent_task.done():
                    if not saw_terminal_event:
                        error_message = "Agent stream ended unexpectedly before emitting a terminal event."
                        if agent_task.cancelled():
                            error_message = "Agent task was cancelled before completion."
                        else:
                            try:
                                exc = agent_task.exception()
                            except Exception:
                                exc = None
                            if exc is not None:
                                error_message = str(exc)
                        yield f"event: error\ndata: {json.dumps({'message': error_message})}\n\n"
                    break
                now = time.monotonic()
                if now - last_heartbeat >= SSE_HEARTBEAT_SECONDS:
                    # Keep long-running responses alive through proxies/browser buffers.
                    yield ": keepalive\n\n"
                    last_heartbeat = now
                continue
    except Exception as e:
        yield f"event: error\ndata: {json.dumps({'message': str(e)})}\n\n"
    finally:
        # Make sure agent task is done
        if not agent_task.done():
            agent_task.cancel()


@router.post("/chat")
async def chat(request: ChatRequest, req: Request):
    """SSE streaming chat endpoint."""
    return StreamingResponse(
        event_generator(
            req,
            request.session_id,
            request.message,
            request.file_ids or [],
            request.reasoning_mode,
            request.audio_input.model_dump() if request.audio_input else None,
            request.audio_url.model_dump() if request.audio_url else None,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
