from collections.abc import AsyncGenerator, Callable
from typing import Annotated, Any

from pydantic import (  # noqa  , SecretStr, EmailStr, computed_field
    Field,
    PostgresDsn,
    model_validator,
)
from pydantic_core import MultiHostUrl  # noqa
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (  # noqa
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool, Pool  # noqa

NonEmptyStr = Annotated[str, Field(min_length=1)]
PositiveInt = Annotated[int, Field(default=1, gt=0)]


class BaseConf(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )


class BaseDBConf(BaseConf):
    DEFAULT: str = "postgres"
    DB_PORT: int = 5432
    # SCHEME: str = "postgresql+psycopg"
    SCHEME: str = "postgresql+asyncpg"
    DB_USER: str = DEFAULT  # | None = None
    DB_PASSWORD: str = DEFAULT  # | None = None
    DB_HOST: str = DEFAULT  # | None = None
    DB_NAME: str = DEFAULT  # | None = None

    @property
    def DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.SCHEME,
            username=self.DB_USER,
            password=self.DB_PASSWORD,  # .get_secret_value(),
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    # def set_defaults(self, fields: str, default: Any) -> None:
    #     for f in fields.split():
    #         if getattr(self, f) is None:
    #             setattr(self, f, default)

    # @model_validator(mode="after")
    # def check_attrs(self) -> "BaseDBConf":
    #     self.set_defaults(
    #         fields="DB_USER DB_PASSWORD DB_HOST DB_NAME",
    #         default=self.DEFAULT,
    #     )
    #     return self

    def get_async_engine_session(
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
