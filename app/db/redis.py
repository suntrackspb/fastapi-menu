import aioredis
from aioredis import Redis

from app.config import REDIS_URL


async def get_cache() -> Redis:
    return aioredis.from_url(
        REDIS_URL,
        max_connections=10,
        encoding='utf8',
        decode_responses=True,
    )


async def cache_init() -> None:
    r = await get_cache()
    await r.flushall()
