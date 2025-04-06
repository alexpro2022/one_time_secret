from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.testdb_config import async_session, engine
from src.models import Base


@pytest.fixture
def override_session(monkeypatch: pytest.MonkeyPatch):
    """General fixture."""
    monkeypatch.setattr("src.services.log.async_session", async_session)


@pytest_asyncio.fixture
async def init_db(override_session):
    """General fixture."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def get_test_session(init_db) -> AsyncGenerator[None, AsyncSession]:
    """General fixture."""
    async with async_session() as s:
        yield s
