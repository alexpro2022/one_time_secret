"""Fixtures for API testing."""

from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from httpx import AsyncClient

from src.config import db_config, testdb_config
from src.fastapi.main import app


@pytest_asyncio.fixture(scope="session")
async def async_client(generic_async_client) -> AsyncGenerator[AsyncClient, Any]:
    async for ac in generic_async_client(app, db_config, testdb_config):
        yield ac
