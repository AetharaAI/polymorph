from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from backend.channels import ChannelManager
from backend.channels.dispatcher import run_channel_turn
from backend.channels.telegram import (
    parse_telegram_update,
    resolve_telegram_config,
    send_telegram_message,
    sync_telegram_webhook,
)

router = APIRouter()


class TelegramWebhookSyncRequest(BaseModel):
    drop_pending_updates: bool = False


@router.get("/channels")
async def list_channels():
    manager = ChannelManager()
    return {
        "control_plane": manager.runtime_summary(),
        "channels": [channel.to_dict() for channel in manager.list_channels()],
    }


@router.get("/channels/{channel_id}")
async def get_channel(channel_id: str):
    manager = ChannelManager()
    channel = manager.get_channel(channel_id)
    if channel is None:
        raise HTTPException(status_code=404, detail=f"Unknown channel '{channel_id}'")
    return {
        "control_plane": manager.runtime_summary(),
        "channel": channel.to_dict(),
    }


@router.post("/channels/telegram/sync-webhook")
async def sync_telegram_channel_webhook(payload: TelegramWebhookSyncRequest):
    config = resolve_telegram_config()
    if not config["configured"]:
        raise HTTPException(status_code=400, detail="Telegram channel is not configured.")
    result = await sync_telegram_webhook(drop_pending_updates=payload.drop_pending_updates)
    return {
        "status": "ok",
        "delivery_mode": config["delivery_mode"],
        "result": result,
    }


@router.post("/channels/telegram/webhook")
async def receive_telegram_webhook(request: Request):
    config = resolve_telegram_config()
    if not config["enabled"]:
        raise HTTPException(status_code=403, detail="Telegram channel is disabled.")
    if not config["configured"]:
        raise HTTPException(status_code=400, detail="Telegram channel is not configured.")

    expected_secret = str(config["webhook_secret"] or "")
    if expected_secret:
        received_secret = str(request.headers.get("X-Telegram-Bot-Api-Secret-Token") or "").strip()
        if received_secret != expected_secret:
            raise HTTPException(status_code=403, detail="Invalid Telegram webhook secret.")

    update = await request.json()
    if not isinstance(update, dict):
        raise HTTPException(status_code=400, detail="Invalid Telegram webhook payload.")

    inbound, ignore_reason = parse_telegram_update(update)
    if inbound is None:
        return {"status": "ignored", "reason": ignore_reason or "Unsupported update."}

    result = await run_channel_turn(inbound)
    if result["status"] == "error":
        return {
            "status": "error",
            "session_id": inbound.session_id,
            "errors": result["errors"],
        }

    assistant_text = str(result.get("assistant_text") or "").strip()
    if not assistant_text:
        assistant_text = "I completed the turn but produced no visible reply."

    telegram_result = await send_telegram_message(
        bot_token=str(config["bot_token"]),
        chat_id=inbound.conversation_id,
        text=assistant_text,
        reply_to_message_id=inbound.message_id,
    )

    return {
        "status": "ok",
        "session_id": inbound.session_id,
        "inbound": inbound.to_dict(),
        "tool_calls": result["tool_calls"],
        "usage": result["usage"],
        "telegram": _summarize_telegram_send(telegram_result),
    }


def _summarize_telegram_send(payload: dict[str, Any]) -> dict[str, Any]:
    result = payload.get("result") if isinstance(payload, dict) else {}
    if not isinstance(result, dict):
        result = {}
    return {
        "ok": bool(payload.get("ok")) if isinstance(payload, dict) else False,
        "message_id": result.get("message_id"),
        "date": result.get("date"),
    }
