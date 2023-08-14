import json
from typing import Any

from aioredis import Redis
from fastapi.encoders import jsonable_encoder

from app.config import REDIS_EXPIRE


class CacheService:
    def __init__(self, cache: Redis):
        self.cache = cache

    async def set_all(self, list_name: str, data: list):
        data = [value.__dict__ for value in data]
        for value in data:
            value.pop("_sa_instance_state", None)
        data_str = json.dumps(jsonable_encoder(data))
        set_cache: str = await self.cache.set(list_name, data_str)
        await self.cache.expire(list_name, REDIS_EXPIRE)
        return set_cache

    async def add(self, key: str, value: Any):
        value = json.dumps(value)
        return await self.cache.set(key, value, ex=REDIS_EXPIRE)

    async def get(self, name: str):
        value = await self.cache.get(name)
        return json.loads(value) if value else None

    async def set(self, name: str, value: str):
        value = jsonable_encoder(value)
        set_cache = await self.cache.set(name, json.dumps(value))
        await self.cache.expire(name, REDIS_EXPIRE)
        return set_cache

    async def delete(self, name: str):
        return await self.cache.delete(name)
