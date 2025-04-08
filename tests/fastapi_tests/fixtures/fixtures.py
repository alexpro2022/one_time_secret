"""Fixtures for API testing."""

from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.config.repositories.db_config import get_async_session
from src.config.repositories.testdb_config import (
    get_async_session as override_get_async_session,
)
from src.main import app

BASE_URL = "http://test"


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, Any]:
    app.dependency_overrides[get_async_session] = override_get_async_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=BASE_URL,
    ) as ac:
        yield ac
