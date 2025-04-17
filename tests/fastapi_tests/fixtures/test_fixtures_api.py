from httpx import AsyncClient
from toolkit.test_tools.base_test_fastapi import API_Router
from toolkit.test_tools.fixtures import BASE_URL
from toolkit.test_tools.utils import assert_equal, assert_isinstance

from src.config import db_config, testdb_config
from src.fastapi.main import app


def test__async_client_fixture(async_client: AsyncClient):
    # Test client
    assert_isinstance(async_client, AsyncClient)
    assert_equal(async_client.base_url, BASE_URL)
    # Test dependencies
    assert_equal(
        actual=app.dependency_overrides,
        expected={db_config.get_async_session: testdb_config.get_async_session},
    )
    assert_equal(API_Router.router, app.router)
