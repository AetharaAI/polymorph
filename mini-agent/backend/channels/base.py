from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ChannelDescriptor:
    channel_id: str
    name: str
    transport: str
    direction: str
    enabled: bool
    configured: bool
    status: str
    details: str = ""
    requires_restart: bool = True
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "name": self.name,
            "transport": self.transport,
            "direction": self.direction,
            "enabled": self.enabled,
            "configured": self.configured,
            "status": self.status,
            "details": self.details,
            "requires_restart": self.requires_restart,
            "capabilities": list(self.capabilities),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ChannelInboundMessage:
    channel_id: str
    session_id: str
    user_id: str
    conversation_id: str
    message_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "conversation_id": self.conversation_id,
            "message_id": self.message_id,
            "text": self.text,
            "metadata": dict(self.metadata),
        }
