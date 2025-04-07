from pydantic import PositiveInt, RedisDsn
from pydantic_core import MultiHostUrl
from redis import Redis  # type: ignore [import]
from redis import asyncio as aioredis  # type: ignore [import]

from src.config.base import BaseConf, NonEmptyStr, SettingsConfigDict


class SettingsRedis(BaseConf):
    model_config = SettingsConfigDict(env_prefix="REDIS_")
    # REDIS_URI: NonEmptyStr = "redis://redis:6379"
    SCHEME: str = "redis"
    HOST: NonEmptyStr = "redis"
    PORT: PositiveInt = 6379
    EXPIRE: PositiveInt = 3600

    @property
    def REDIS_URI(self) -> RedisDsn:
        return MultiHostUrl.build(
            scheme=self.SCHEME,
            host=self.HOST,
            port=self.PORT,
        )


redis_conf = SettingsRedis()


def get_aioredis() -> aioredis.Redis:
    return aioredis.from_url(str(redis_conf.REDIS_URI), decode_responses=True)


def get_redis():
    return Redis(host=redis_conf.HOST, port=redis_conf.PORT, db=0)
