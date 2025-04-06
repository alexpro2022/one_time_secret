from src.config.app_config import app_conf
from src.models import Secret
from tests.testing_tools import BaseTest_CRUD, BaseTest_Model, Data

secret_test_data = Data(
    model=Secret,
    create_data={"secret": "доступ_к_конфиденциальным_данным"},
    default_data={"ttl_seconds": app_conf.secret_min_ttl},
    nullable_fields=["passphrase"],
)


class Test_SecretModel(BaseTest_Model):
    data = secret_test_data


class Test_SecretCRUD(BaseTest_CRUD):
    data = secret_test_data
