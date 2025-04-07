from redis import Redis  # type: ignore [import]
from redis import asyncio as aioredis  # type: ignore [import]

REDIS_URL = "redis://redis:6379"


def get_aioredis() -> aioredis.Redis:
    return aioredis.from_url(REDIS_URL, decode_responses=True)


def get_redis():
    return Redis(host="redis", port="6379", db=0)
