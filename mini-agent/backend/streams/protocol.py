from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class MessageType(str, Enum):
    EVENT = "event"
    COMMAND = "command"
    RESPONSE = "response"


class StreamMessage:
    def __init__(
        self,
        *,
        source_model: str,
        target_model: str = "*",
        msg_type: MessageType = MessageType.EVENT,
        payload: dict[str, Any] | None = None,
        harness_id: str = "polymorph-internal",
        trace_id: str | None = None,
        correlation_id: str | None = None,
    ):
        self.trace_id = trace_id or uuid.uuid4().hex
        self.correlation_id = correlation_id
        self.source_model = source_model
        self.target_model = target_model
        self.msg_type = msg_type
        self.payload = payload or {}
        self.harness_id = harness_id
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_redis_fields(self) -> dict[str, str]:
        return {
            "trace_id": self.trace_id,
            "correlation_id": self.correlation_id or "",
            "source_model": self.source_model,
            "target_model": self.target_model,
            "type": self.msg_type.value,
            "payload": json.dumps(self.payload, ensure_ascii=False, default=str),
            "harness_id": self.harness_id,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_redis_entry(cls, entry: dict[str, str]) -> StreamMessage:
        msg = cls(
            source_model=entry.get("source_model", ""),
            target_model=entry.get("target_model", "*"),
            msg_type=MessageType(entry.get("type", "event")),
            payload=json.loads(entry.get("payload", "{}")),
            harness_id=entry.get("harness_id", ""),
            trace_id=entry.get("trace_id"),
            correlation_id=entry.get("correlation_id") or None,
        )
        msg.timestamp = entry.get("timestamp", msg.timestamp)
        return msg

    def __repr__(self) -> str:
        return (
            f"StreamMessage(type={self.msg_type.value}, "
            f"source={self.source_model}, target={self.target_model}, "
            f"trace={self.trace_id[:8]})"
        )
