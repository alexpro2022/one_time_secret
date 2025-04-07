from src.config import app_config, cache_config, db_config, testdb_config
from tests.testing_tools import BaseTest_Config, BaseTest_DBConfig


class Test_AppConfig(BaseTest_Config):
    module = app_config
    conf_name = "app_conf"
    conf_fields = {
        "url_prefix": "/api/v1",
    }


class Test_RedisConfig(BaseTest_Config):
    module = cache_config
    conf_name = "redis_conf"


class Test_DBConfig(BaseTest_DBConfig):
    module = db_config


class Test_TestDBConfig(BaseTest_DBConfig):
    module = testdb_config
