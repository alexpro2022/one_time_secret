from collections.abc import AsyncGenerator, Callable
from typing import Any

from pydantic import PositiveInt, PostgresDsn, RedisDsn
from pydantic_core import MultiHostUrl  # noqa
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import Redis  # type: ignore [import]
from redis import asyncio as aioredis  # type: ignore [import]
from sqlalchemy.ext.asyncio import (  # noqa
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool, Pool  # noqa

from src.types_app import NonEmptyStr


# ====================================================
class BaseConf(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )


# ====================================================
class BaseDBConf(BaseConf):
    DEFAULT: str = "github_actions"
    SCHEME: str = "postgresql+asyncpg"
    USER: str = DEFAULT
    PASSWORD: str = DEFAULT
    HOST: str = DEFAULT
    PORT: int = 5432
    NAME: str = DEFAULT

    @property
    def DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.SCHEME,
            username=self.USER,
            password=self.PASSWORD,  # .get_secret_value(),
            host=self.HOST,
            port=self.PORT,
            path=self.NAME,
        )

    def get_dependencies(
        self,
        echo: bool = False,
        expire_on_commit: bool = False,
        autoflush: bool = True,
        poolclass: Pool | None = None,
        # https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
    ) -> tuple[
        AsyncEngine,
        async_sessionmaker[AsyncSession],
        Callable[[], AsyncGenerator[Any, None]],
    ]:
        engine = create_async_engine(
            url=str(self.DATABASE_URI),
            **{"poolclass": poolclass} if poolclass is not None else {},
            echo=echo,
        )

        async_session = async_sessionmaker(
            bind=engine,
            expire_on_commit=expire_on_commit,
            autoflush=autoflush,
        )

        async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
            async with async_session.begin() as s:
                yield s
                assert s.in_transaction()

        return engine, async_session, get_async_session


# ====================================================
class BaseRedisConf(BaseConf):
    model_config = SettingsConfigDict(env_prefix="REDIS_")
    SCHEME: NonEmptyStr = "redis"
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

    def get_dependencies(self):
        def get_aioredis() -> aioredis.Redis:
            return aioredis.from_url(str(self.REDIS_URI), decode_responses=True)

        def get_redis():
            return Redis(host=self.HOST, port=self.PORT, db=0)

        return get_aioredis, get_redis
