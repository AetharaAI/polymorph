from __future__ import annotations

import json
import time
from typing import Any

import redis.asyncio as aioredis

REGISTRY_KEY = "polymorph:models:registry"
HEARTBEAT_TTL_SECONDS = 120


class ModelRegistry:
    def __init__(self, redis: aioredis.Redis, harness_id: str = "polymorph-internal"):  # type: ignore[type-arg]
        self.redis = redis
        self.harness_id = harness_id

    async def register(
        self,
        model_id: str,
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        entry = json.dumps({
            "model_id": model_id,
            "harness_id": self.harness_id,
            "capabilities": capabilities or [],
            "metadata": metadata or {},
            "last_heartbeat": time.time(),
        })
        await self.redis.hset(REGISTRY_KEY, model_id, entry)

    async def heartbeat(self, model_id: str) -> None:
        raw = await self.redis.hget(REGISTRY_KEY, model_id)
        if not raw:
            await self.register(model_id)
            return
        data = json.loads(raw)
        data["last_heartbeat"] = time.time()
        await self.redis.hset(REGISTRY_KEY, model_id, json.dumps(data))

    async def list_models(self, only_alive: bool = True) -> list[dict[str, Any]]:
        all_entries = await self.redis.hgetall(REGISTRY_KEY)
        now = time.time()
        models: list[dict[str, Any]] = []
        for _key, raw in all_entries.items():
            data = json.loads(raw)
            alive = (now - data.get("last_heartbeat", 0)) < HEARTBEAT_TTL_SECONDS
            data["alive"] = alive
            if only_alive and not alive:
                continue
            models.append(data)
        return models

    async def get_model(self, model_id: str) -> dict[str, Any] | None:
        raw = await self.redis.hget(REGISTRY_KEY, model_id)
        if not raw:
            return None
        return json.loads(raw)

    async def unregister(self, model_id: str) -> None:
        await self.redis.hdel(REGISTRY_KEY, model_id)
