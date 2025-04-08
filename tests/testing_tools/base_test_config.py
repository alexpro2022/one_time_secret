from collections.abc import AsyncGenerator
from typing import Any

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from tests.testing_tools.utils import assert_equal, assert_isinstance


class BaseTest_Config:
    """
    Attributes:
        module - module imported from config as below:
    ```
    from src.config import db_config, testdb_config
    ```
    """

    module: Any
    conf_name: str
    conf_fields: dict[str, Any] = {}

    def get_attr(self, attr_name: str):
        attr = getattr(self.module, attr_name, None)
        assert attr is not None
        return attr

    def test__conf(self):
        conf = self.get_attr(self.conf_name)
        assert_isinstance(conf, BaseSettings)

    def test__fields(self):
        conf = self.get_attr(self.conf_name)
        for field in self.conf_fields:
            assert_equal(getattr(conf, field, None), self.conf_fields[field])


class BaseTest_DBConfig(BaseTest_Config):
    conf_name = "db_conf"

    async def test__engine(self):
        engine = self.get_attr("engine")
        assert_isinstance(engine, AsyncEngine)

    async def test__async_session(self):
        async_session = self.get_attr("async_session")
        assert_isinstance(async_session, async_sessionmaker)
        async with async_session() as s:
            assert_isinstance(s, AsyncSession)

    async def test__get_async_session(self):
        get_async_session = self.get_attr("get_async_session")()
        assert_isinstance(get_async_session, AsyncGenerator)
        async for s in get_async_session:
            assert_isinstance(s, AsyncSession)
            assert s.in_transaction()
