from __future__ import annotations

import os
from typing import Mapping, Any

import httpx

from .base import ChannelDescriptor, ChannelInboundMessage


TELEGRAM_API_BASE = "https://api.telegram.org"


def _clean(value: str | None) -> str:
    return (value or "").strip()


def _truthy(value: str | None, default: bool = False) -> bool:
    raw = _clean(value)
    if not raw:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}


def _split_csv(value: str | None) -> list[str]:
    raw = _clean(value)
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def resolve_telegram_config(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    source = env if env is not None else os.environ
    enabled = _truthy(source.get("CHANNELS_TELEGRAM_ENABLED"), default=False)
    bot_token = _clean(source.get("CHANNELS_TELEGRAM_BOT_TOKEN"))
    webhook_url = _clean(source.get("CHANNELS_TELEGRAM_WEBHOOK_URL"))
    webhook_secret = _clean(source.get("CHANNELS_TELEGRAM_WEBHOOK_SECRET"))
    allowed_chat_ids = _split_csv(source.get("CHANNELS_TELEGRAM_ALLOWED_CHAT_IDS"))
    session_scope = _clean(source.get("CHANNELS_TELEGRAM_SESSION_SCOPE")) or "chat"

    configured = bool(bot_token)
    if enabled and configured:
        status = "configured"
        details = "Telegram adapter is configured and ready for runtime wiring."
    elif enabled and not configured:
        status = "degraded"
        details = "Telegram adapter is enabled but missing CHANNELS_TELEGRAM_BOT_TOKEN."
    elif configured:
        status = "configured"
        details = "Telegram credentials are present but the adapter is disabled."
    else:
        status = "disabled"
        details = "Telegram adapter is disabled."

    return {
        "enabled": enabled,
        "configured": configured,
        "status": status,
        "details": details,
        "bot_token": bot_token,
        "webhook_url": webhook_url,
        "webhook_secret": webhook_secret,
        "allowed_chat_ids": allowed_chat_ids,
        "session_scope": session_scope,
        "delivery_mode": "webhook" if webhook_url else "polling",
    }


def build_telegram_descriptor(env: Mapping[str, str] | None = None) -> ChannelDescriptor:
    config = resolve_telegram_config(env)
    return ChannelDescriptor(
        channel_id="telegram",
        name="Telegram",
        transport="bot_api",
        direction="bidirectional",
        enabled=bool(config["enabled"]),
        configured=bool(config["configured"]),
        status=str(config["status"]),
        details=str(config["details"]),
        requires_restart=True,
        capabilities=["text", "media", "dm", "group"],
        metadata={
            "delivery_mode": config["delivery_mode"],
            "session_scope": config["session_scope"],
            "allowed_chat_count": len(config["allowed_chat_ids"]),
            "webhook_configured": bool(config["webhook_url"]),
            "webhook_secret_configured": bool(config["webhook_secret"]),
        },
    )


def build_telegram_session_id(chat_id: str, user_id: str, scope: str) -> str:
    normalized_scope = (scope or "chat").strip().lower()
    if normalized_scope == "user":
        return f"telegram:user:{user_id}"
    return f"telegram:chat:{chat_id}"


def parse_telegram_update(update: dict[str, Any], env: Mapping[str, str] | None = None) -> tuple[ChannelInboundMessage | None, str | None]:
    config = resolve_telegram_config(env)
    message = update.get("message") or update.get("edited_message")
    if not isinstance(message, dict):
        return None, "No supported Telegram message payload found."

    chat = message.get("chat") if isinstance(message.get("chat"), dict) else {}
    user = message.get("from") if isinstance(message.get("from"), dict) else {}
    text = _clean(message.get("text") or message.get("caption"))
    if not text:
        return None, "Telegram update has no text/caption content."

    chat_id = str(chat.get("id") or "").strip()
    user_id = str(user.get("id") or "").strip()
    message_id = str(message.get("message_id") or update.get("update_id") or "").strip()
    if not chat_id or not user_id or not message_id:
        return None, "Telegram update is missing chat/user/message identifiers."

    allowed_chat_ids = set(config["allowed_chat_ids"])
    if allowed_chat_ids and chat_id not in allowed_chat_ids:
        return None, f"Chat {chat_id} is not in CHANNELS_TELEGRAM_ALLOWED_CHAT_IDS."

    envelope = ChannelInboundMessage(
        channel_id="telegram",
        session_id=build_telegram_session_id(chat_id, user_id, str(config["session_scope"])),
        user_id=user_id,
        conversation_id=chat_id,
        message_id=message_id,
        text=text,
        metadata={
            "update_id": update.get("update_id"),
            "chat_type": chat.get("type"),
            "chat_title": chat.get("title"),
            "username": user.get("username"),
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
        },
    )
    return envelope, None


async def send_telegram_message(
    *,
    bot_token: str,
    chat_id: str,
    text: str,
    reply_to_message_id: str | None = None,
    timeout_seconds: float = 20.0,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "chat_id": chat_id,
        "text": text[:4096],
    }
    if reply_to_message_id:
        try:
            payload["reply_to_message_id"] = int(reply_to_message_id)
        except Exception:
            pass

    url = f"{TELEGRAM_API_BASE}/bot{bot_token}/sendMessage"
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        resp = await client.post(url, json=payload)
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        if resp.is_success and isinstance(data, dict) and data.get("ok") is True:
            return data
        raise RuntimeError(f"Telegram sendMessage failed: HTTP {resp.status_code} {str(data)[:300]}")


async def sync_telegram_webhook(
    *,
    env: Mapping[str, str] | None = None,
    drop_pending_updates: bool = False,
    timeout_seconds: float = 20.0,
) -> dict[str, Any]:
    config = resolve_telegram_config(env)
    if not config["bot_token"]:
        raise RuntimeError("CHANNELS_TELEGRAM_BOT_TOKEN is required.")

    bot_token = str(config["bot_token"])
    webhook_url = str(config["webhook_url"])
    webhook_secret = str(config["webhook_secret"])

    if webhook_url:
        endpoint = f"{TELEGRAM_API_BASE}/bot{bot_token}/setWebhook"
        payload: dict[str, Any] = {
            "url": webhook_url.rstrip("/"),
            "drop_pending_updates": drop_pending_updates,
        }
        if webhook_secret:
            payload["secret_token"] = webhook_secret
    else:
        endpoint = f"{TELEGRAM_API_BASE}/bot{bot_token}/deleteWebhook"
        payload = {"drop_pending_updates": drop_pending_updates}

    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        resp = await client.post(endpoint, json=payload)
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        if resp.is_success and isinstance(data, dict) and data.get("ok") is True:
            return data
        raise RuntimeError(f"Telegram webhook sync failed: HTTP {resp.status_code} {str(data)[:300]}")
