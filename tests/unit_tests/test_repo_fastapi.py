from src.repo.models import Secret
from tests.testing_tools import BaseTest_CRUD, BaseTest_Model, Data

secret_test_data = Data(
    model=Secret,
    create_data={"secret": "доступ_к_конфиденциальным_данным"},
    nullable_fields=["passphrase", "ttl_seconds"],
)


class Test_SecretModel(BaseTest_Model):
    data = secret_test_data


class Test_SecretCRUD(BaseTest_CRUD):
    data = secret_test_data
