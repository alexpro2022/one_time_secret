from src.config import app_config
from tests.testing_tools import BaseTest_Config


class Test_AppConfig(BaseTest_Config):
    module = app_config
    conf_name = "app_conf"
    conf_fields = {
        "url_prefix": "/api/v1",
        "secret_min_ttl": 1,
    }
