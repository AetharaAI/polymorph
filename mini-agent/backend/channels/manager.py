from __future__ import annotations

import os
from typing import Any

from .base import ChannelDescriptor
from .telegram import build_telegram_descriptor


def _clean(value: str | None) -> str:
    return (value or "").strip()


def _truthy(value: str | None, default: bool = False) -> bool:
    raw = _clean(value)
    if not raw:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}


class ChannelManager:
    def __init__(self) -> None:
        self._builders = {
            "telegram": build_telegram_descriptor,
        }

    def runtime_summary(self) -> dict[str, Any]:
        enabled = _truthy(os.getenv("CHANNELS_RUNTIME_ENABLED"), default=False)
        default_route = _clean(os.getenv("CHANNELS_DEFAULT_ROUTE")) or "agent_chat"
        session_namespace = _clean(os.getenv("CHANNELS_SESSION_NAMESPACE")) or "channel_conversation"
        return {
            "enabled": enabled,
            "status": "configured" if enabled else "disabled",
            "default_route": default_route,
            "session_namespace": session_namespace,
            "channel_count": len(self._builders),
        }

    def list_channels(self) -> list[ChannelDescriptor]:
        return [builder() for builder in self._builders.values()]

    def get_channel(self, channel_id: str) -> ChannelDescriptor | None:
        builder = self._builders.get((channel_id or "").strip().lower())
        if not builder:
            return None
        return builder()
