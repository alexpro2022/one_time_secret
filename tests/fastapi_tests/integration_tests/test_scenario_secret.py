from uuid import UUID

from httpx import AsyncClient

from src.api.endpoints import log, secret
from src.api.schemas.log import Log as log_schema
from tests.fastapi_tests.integration_tests.test_api_secret import MSG_NOT_FOUND
from tests.testing_tools.base_test_fastapi import HTTPMethod, request
from tests.testing_tools.utils import assert_equal
from tests.unit_tests.test_repo_fastapi import secret_test_data as DATA


async def test_scenario(init_db, async_client: AsyncClient):
    """
    Scenario:
      - Create
      - Get one - OK
      - Get one - not found
      - Create
      - Delete - OK
      - Get one - not found
    """

    async def post_request():
        """Create new secret."""
        return await request(
            async_client,
            http_method=HTTPMethod.POST,
            path_func=secret.create_secret,
            json=DATA.create_data_json,
            expected_status_code=201,
        )

    async def get_request_not_found():
        """Check secret not found."""
        return await request(
            async_client,
            http_method=HTTPMethod.GET,
            path_func=secret.get_secret,
            secret_key=secret_key,
            expected_status_code=404,
            expected_response_json={
                "detail": MSG_NOT_FOUND.format(item_id=repr(UUID(secret_key)))
            },
        )

    # Test GET one time
    secret_key = (await post_request()).json().get("secret_key")
    await request(
        async_client,
        http_method=HTTPMethod.GET,
        path_func=secret.get_secret,
        secret_key=secret_key,
        expected_response_json={"secret": DATA.create_data["secret"]},
    )
    assert await get_request_not_found()

    # Test DELETE
    secret_key = (await post_request()).json().get("secret_key")
    await request(
        async_client,
        http_method=HTTPMethod.DELETE,
        path_func=secret.get_secret,
        secret_key=secret_key,
        expected_response_json={"status": "secret_deleted"},
    )
    assert await get_request_not_found()

    # Tests LOG
    logs = (
        await request(
            async_client,
            http_method=HTTPMethod.GET,
            path_func=log.get_logs,
        )
    ).json()
    assert logs
    assert_equal(len(logs), 5)
    for logged in logs:
        log_schema.model_validate(logged)
