from httpx import AsyncClient

from tests.fastapi_tests.fixtures.fixtures import (
    BASE_URL,
    app,
    get_async_session,
    override_get_async_session,
)
from tests.testing_tools.utils import assert_equal, assert_isinstance


def test__async_client_fixture(async_client):
    assert_equal(
        app.dependency_overrides, {get_async_session: override_get_async_session}
    )
    assert_isinstance(async_client, AsyncClient)
    assert_equal(async_client.base_url, BASE_URL)
