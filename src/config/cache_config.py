from redis import Redis  # type: ignore [import]
from redis import asyncio as aioredis  # type: ignore [import]

from src.config.base import BaseConf, NonEmptyStr, PositiveInt


class SettingsRedis(BaseConf):
    REDIS_URI: NonEmptyStr = "redis://redis:6379"
    expire: PositiveInt = 3600


redis_conf = SettingsRedis()


def get_aioredis() -> aioredis.Redis:
    return aioredis.from_url(redis_conf.REDIS_URI, decode_responses=True)


def get_redis():
    return Redis(host="redis", port="6379", db=0)
