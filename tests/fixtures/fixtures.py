from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.testdb_config import async_session, engine
from src.repo.models import Base


@pytest_asyncio.fixture
async def init_db():
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
