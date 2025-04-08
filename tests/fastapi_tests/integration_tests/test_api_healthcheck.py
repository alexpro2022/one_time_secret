from src import main
from tests.testing_tools.base_test_fastapi import BaseTest_API, HTTPMethod


class Test_Healthcheck(BaseTest_API):
    http_method = HTTPMethod.GET
    path_func = main.healthcheck
    expected_response_json = {"message": "OK"}
