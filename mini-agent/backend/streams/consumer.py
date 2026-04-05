from __future__ import annotations

import asyncio
from typing import Awaitable, Callable

from backend.streams.client import StreamClient
from backend.streams.protocol import StreamMessage
from backend.streams.registry import ModelRegistry


class StreamConsumer:
    def __init__(
        self,
        client: StreamClient,
        registry: ModelRegistry,
        model_id: str,
        on_command: Callable[[StreamMessage], Awaitable[StreamMessage | None]] | None = None,
    ):
        self.client = client
        self.registry = registry
        self.model_id = model_id
        self.on_command = on_command
        self._running = False
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        await self.client.ensure_consumer_groups()
        await self.registry.register(self.model_id)
        self._running = True
        self._task = asyncio.create_task(self._loop())
        print(f"[StreamConsumer:{self.model_id}] Started", flush=True)

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        await self.registry.unregister(self.model_id)
        print(f"[StreamConsumer:{self.model_id}] Stopped", flush=True)

    async def _loop(self) -> None:
        while self._running:
            try:
                await self.registry.heartbeat(self.model_id)

                commands = await self.client.read_commands(count=5, block_ms=1000)
                for entry_id, msg in commands:
                    print(
                        f"[StreamConsumer:{self.model_id}] Command received: "
                        f"from={msg.source_model} trace={msg.trace_id[:8]}",
                        flush=True,
                    )
                    if self.on_command:
                        try:
                            response = await self.on_command(msg)
                            if response:
                                await self.client.publish_response(response)
                        except Exception as exc:  # noqa: BLE001
                            print(
                                f"[StreamConsumer:{self.model_id}] Command handler error: {exc}",
                                flush=True,
                            )
                    await self.client.ack_command(entry_id)

            except asyncio.CancelledError:
                break
            except Exception as exc:  # noqa: BLE001
                print(f"[StreamConsumer:{self.model_id}] Loop error: {exc}", flush=True)
                await asyncio.sleep(2)
