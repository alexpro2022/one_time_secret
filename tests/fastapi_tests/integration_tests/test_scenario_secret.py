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


"""
 [
 {
 'id': 'df7a8306-229f-44a4-b7ce-735deb24115d',
 'client_info': '127.0.0.1:123',
 'event_time': '2025-04-06T12:54:37.364341',
 'secret_id': '83de94f5-0a8d-483b-b0b3-c68a1d2085a5',
 'event': 'created'
 },
 {'id': 'cf5f656e-af17-4657-be22-29b17d10f529', 'client_info': '127.0.0.1:123', 'event_time': '2025-04-06T12:54:37.444337', 'secret_id': '83de94f5-0a8d-483b-b0b3-c68a1d2085a5', 'event': 'read'}, {'id': '6b5d7786-be0f-4a9a-91d0-c8a643be9d25', 'client_info': '127.0.0.1:123', 'event_time': '2025-04-06T12:54:37.463482', 'secret_id': '83de94f5-0a8d-483b-b0b3-c68a1d2085a5', 'event': 'deleted'}, {'id': 'ec6a00aa-5be9-46a7-997d-ab3863037220', 'client_info': '127.0.0.1:123', 'event_time': '2025-04-06T12:54:37.586900', 'secret_id': '7f90e766-222d-4b6e-894a-4e73129488d7', 'event': 'created'}, {'id': '505f349d-5422-436c-bc8e-ad2cb5d29d31', 'client_info': '127.0.0.1:123', 'event_time': '2025-04-06T12:54:37.671284', 'secret_id': '7f90e766-222d-4b6e-894a-4e73129488d7', 'event': 'deleted'}]

"""
