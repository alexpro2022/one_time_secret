from typing import Any

from fastapi import status

from src.api.endpoints import secret, utils
from tests.testing_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from tests.testing_tools.mixins import DBMixin
from tests.unit_tests.test_repo_fastapi import secret_test_data as DATA

PATH_PARAMS = dict(secret_key=DATA.item_uuid)
MSG_NOT_FOUND = "Object with attributes {{'id': {item_id}}} not found"
DETAIL_NOT_FOUND = {"detail": MSG_NOT_FOUND.format(item_id=repr(DATA.item_uuid))}


# MIXINS ===================================================
class PathParamsMixin:
    path_params: dict[str, Any] = PATH_PARAMS


class NotFoundMixin(PathParamsMixin):
    expected_status_code: int = status.HTTP_404_NOT_FOUND
    expected_response_json: dict[str, Any] | None = DETAIL_NOT_FOUND


class ClientNoCacheMixin:
    expected_response_headers: dict[str, str] = utils.CLIENT_NO_CACHE


class API_DB(DBMixin, BaseTest_API):
    """Create obj in DB."""

    db_save_obj = DATA.get_test_obj


# TESTS ======================================================
class Test_GetSecretNotFound(NotFoundMixin, BaseTest_API):
    http_method = HTTPMethod.GET
    path_func = secret.get_secret


class Test_DeleteSecretNotFound(NotFoundMixin, BaseTest_API):
    http_method = HTTPMethod.DELETE
    path_func = secret.delete_secret


class Test_DeleteSecretWrongPassphrase(PathParamsMixin, API_DB):
    http_method = HTTPMethod.DELETE
    path_func = secret.delete_secret
    query_params = dict(passphrase="wrong")
    expected_status_code = status.HTTP_400_BAD_REQUEST
    expected_response_json = {"detail": "Passphrase is missing or incorrect"}


class Test_CreateSecret(ClientNoCacheMixin, BaseTest_API):
    http_method = HTTPMethod.POST
    path_func = secret.create_secret
    json = DATA.create_data_json
    expected_status_code = status.HTTP_201_CREATED


class Test_GetSecret(PathParamsMixin, ClientNoCacheMixin, API_DB):
    http_method = HTTPMethod.GET
    path_func = secret.get_secret
    expected_response_json = {"secret": DATA.expected_response_json_create["secret"]}


class Test_DeleteSecret(PathParamsMixin, ClientNoCacheMixin, API_DB):
    http_method = HTTPMethod.DELETE
    path_func = secret.delete_secret
    expected_response_json = {"status": "secret_deleted"}
