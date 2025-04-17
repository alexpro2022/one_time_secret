from toolkit.test_tools import BaseTest_CRUD, BaseTest_Model, Data

from src.config import app_conf
from src.models import Secret
from src.services.cipher import encrypt

secret_test_data = Data(
    model=Secret,
    create_data={"secret": encrypt("доступ_к_конфиденциальным_данным")},
    default_data={"ttl_seconds": app_conf.secret_min_ttl},
    nullable_fields=["passphrase"],
)


class Test_SecretModel(BaseTest_Model):
    data = secret_test_data


class Test_SecretCRUD(BaseTest_CRUD):
    data = secret_test_data
