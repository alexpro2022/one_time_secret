from src.config import db_config, testdb_config
from tests.testing_tools import BaseTest_DBConfig


class Test_DBConfig(BaseTest_DBConfig):
    module = db_config


class Test_TestDBConfig(BaseTest_DBConfig):
    module = testdb_config
    conf_fields = {
        "DEFAULT_FOR_GH_ACTIONS": "github_actions",
    }
