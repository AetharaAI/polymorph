from __future__ import annotations

import redis.asyncio as aioredis

from backend.streams.protocol import StreamMessage


class StreamClient:
    def __init__(
        self,
        redis: aioredis.Redis,  # type: ignore[type-arg]
        harness_id: str = "polymorph-internal",
        model_id: str = "",
    ):
        self.redis = redis
        self.harness_id = harness_id
        self.model_id = model_id

    def _events_key(self) -> str:
        return f"polymorph:stream:{self.harness_id}:events"

    def _commands_key(self) -> str:
        return f"polymorph:stream:{self.harness_id}:commands"

    def _responses_key(self) -> str:
        return f"polymorph:stream:{self.harness_id}:responses"

    def _consumer_group(self) -> str:
        return f"cg:{self.model_id}"

    async def publish_event(self, msg: StreamMessage) -> str:
        fields = msg.to_redis_fields()
        entry_id = await self.redis.xadd(self._events_key(), fields, maxlen=5000)
        return str(entry_id)

    async def publish_command(self, msg: StreamMessage) -> str:
        fields = msg.to_redis_fields()
        entry_id = await self.redis.xadd(self._commands_key(), fields, maxlen=2000)
        return str(entry_id)

    async def publish_response(self, msg: StreamMessage) -> str:
        fields = msg.to_redis_fields()
        entry_id = await self.redis.xadd(self._responses_key(), fields, maxlen=2000)
        return str(entry_id)

    async def ensure_consumer_groups(self) -> None:
        for key in (self._events_key(), self._commands_key(), self._responses_key()):
            try:
                await self.redis.xgroup_create(key, self._consumer_group(), id="0", mkstream=True)
            except aioredis.ResponseError as exc:
                if "BUSYGROUP" not in str(exc):
                    raise

    async def read_commands(
        self,
        count: int = 10,
        block_ms: int | None = None,
    ) -> list[tuple[str, StreamMessage]]:
        # NOTE: In Redis, block=0 means "block forever". Only pass block
        # when we actually want to wait; omit it for non-blocking reads.
        kwargs: dict = {
            "groupname": self._consumer_group(),
            "consumername": self.model_id,
            "streams": {self._commands_key(): ">"},
            "count": count,
        }
        if block_ms is not None and block_ms > 0:
            kwargs["block"] = block_ms
        entries = await self.redis.xreadgroup(**kwargs)
        results: list[tuple[str, StreamMessage]] = []
        for _stream_name, messages in entries or []:
            for entry_id, fields in messages:
                msg = StreamMessage.from_redis_entry(fields)
                if msg.target_model in (self.model_id, "*"):
                    results.append((str(entry_id), msg))
        return results

    async def ack_command(self, entry_id: str) -> None:
        await self.redis.xack(self._commands_key(), self._consumer_group(), entry_id)

    async def read_events(
        self,
        count: int = 50,
        block_ms: int | None = None,
    ) -> list[tuple[str, StreamMessage]]:
        kwargs: dict = {
            "groupname": self._consumer_group(),
            "consumername": self.model_id,
            "streams": {self._events_key(): ">"},
            "count": count,
        }
        if block_ms is not None and block_ms > 0:
            kwargs["block"] = block_ms
        entries = await self.redis.xreadgroup(**kwargs)
        results: list[tuple[str, StreamMessage]] = []
        for _stream_name, messages in entries or []:
            for entry_id, fields in messages:
                msg = StreamMessage.from_redis_entry(fields)
                results.append((str(entry_id), msg))
                await self.redis.xack(self._events_key(), self._consumer_group(), entry_id)
        return results

    async def read_responses(
        self,
        correlation_id: str,
        timeout_ms: int = 5000,
        poll_interval_ms: int = 100,
    ) -> StreamMessage | None:
        elapsed = 0
        while elapsed < timeout_ms:
            block = min(poll_interval_ms, timeout_ms - elapsed)
            entries = await self.redis.xreadgroup(
                groupname=self._consumer_group(),
                consumername=self.model_id,
                streams={self._responses_key(): ">"},
                count=50,
                block=block,
            )
            for _stream_name, messages in entries or []:
                for entry_id, fields in messages:
                    msg = StreamMessage.from_redis_entry(fields)
                    await self.redis.xack(self._responses_key(), self._consumer_group(), entry_id)
                    if msg.correlation_id == correlation_id:
                        return msg
            elapsed += poll_interval_ms
        return None
