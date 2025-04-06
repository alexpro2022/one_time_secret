from fastapi import status

from src.api.endpoints import secret
from src.config.app_config import app_conf
from tests.testing_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from tests.testing_tools.mixins import (
    ClientNoCacheMixin,
    DBMixin,
    NotFoundMixin,
    PathParamsMixin,
)
from tests.unit_tests.test_repo_fastapi import secret_test_data as DATA

PATH_PARAMS = dict(secret_key=DATA.item_uuid)
MSG_NOT_FOUND = "Object with attributes {{'id': {item_id}}} not found"
DETAIL_NOT_FOUND = {"detail": MSG_NOT_FOUND.format(item_id=repr(DATA.item_uuid))}


# MIXINS ==================================================
PathParamsMixin.path_params = PATH_PARAMS
NotFoundMixin.expected_response_json = DETAIL_NOT_FOUND


class API_DB(DBMixin, BaseTest_API):
    """Create obj in DB."""

    db_save_obj = DATA.get_test_obj


class NotFound(PathParamsMixin, NotFoundMixin, BaseTest_API): ...


class Found(PathParamsMixin, ClientNoCacheMixin, API_DB): ...


# TESTS ======================================================
class Test_GetSecretNotFound(NotFound):
    http_method = HTTPMethod.GET
    path_func = secret.get_secret


class Test_GetSecret(Found):
    http_method = HTTPMethod.GET
    path_func = secret.get_secret
    expected_response_json = {"secret": DATA.expected_response_json_create["secret"]}


class Test_DeleteSecretNotFound(NotFound):
    http_method = HTTPMethod.DELETE
    path_func = secret.delete_secret


class Test_DeleteSecret(Found):
    http_method = HTTPMethod.DELETE
    path_func = secret.delete_secret
    expected_response_json = {"status": "secret_deleted"}


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


class Test_CreateSecretLesserTTL(BaseTest_API):
    http_method = HTTPMethod.POST
    path_func = secret.create_secret
    json = {**DATA.create_data_json, **dict(ttl_seconds=app_conf.secret_min_ttl - 1)}
    expected_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
