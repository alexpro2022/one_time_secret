from src.api.endpoints import secret
from tests.testing_tools.base_test_fastapi import BaseTest_API, HTTPMethod
from tests.testing_tools.mixins import DBMixin
from tests.unit_tests.test_repo_fastapi import secret_test_data as DATA

PATH_PARAMS = dict(secret_key=DATA.item_uuid)
MSG_NOT_FOUND = "Object with attributes {{'id': {item_id}}} not found"
DETAIL_NOT_FOUND = {"detail": MSG_NOT_FOUND.format(item_id=repr(DATA.item_uuid))}


class API_DB(DBMixin, BaseTest_API):
    """Creating obj in DB."""

    db_save_obj = DATA.get_test_obj


class Test_GetSecretNotFound(BaseTest_API):
    http_method = HTTPMethod.GET
    path_func = secret.get_secret
    path_params = PATH_PARAMS
    expected_status_code = 404
    expected_response_json = DETAIL_NOT_FOUND


class Test_GetSecret(API_DB):
    http_method = HTTPMethod.GET
    path_func = secret.get_secret
    path_params = PATH_PARAMS
    expected_response_json = {"secret": DATA.expected_response_json_create["secret"]}


class Test_DeleteSecretNotFound(BaseTest_API):
    http_method = HTTPMethod.DELETE
    path_func = secret.delete_secret
    path_params = PATH_PARAMS
    expected_status_code = 404
    expected_response_json = DETAIL_NOT_FOUND


class Test_DeleteSecretWrongPassphrase(API_DB):
    http_method = HTTPMethod.DELETE
    path_func = secret.delete_secret
    path_params = PATH_PARAMS
    query_params = dict(passphrase="wrong")
    expected_status_code = 400
    expected_response_json = {"detail": "Passphrase is missing or incorrect"}


class Test_DeleteSecret(API_DB):
    http_method = HTTPMethod.DELETE
    path_func = secret.delete_secret
    path_params = PATH_PARAMS
    expected_response_json = {"status": "secret_deleted"}


class Test_CreateSecret(BaseTest_API):
    http_method = HTTPMethod.POST
    path_func = secret.create_secret
    json = DATA.create_data_json
    expected_status_code = 201
