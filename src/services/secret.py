from src.repo.db import crud
from src.repo.models import Secret as repo_model
from src.types_app import _AS, JsonType


async def create(session: _AS, **create_data) -> JsonType:
    """
    После успешного создания секрета сервис должен:
    \n  * Сохранить секрет.
    \n  * Залогировать создание секрета в PostgreSQL (например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.).
    """
    assert session.in_transaction()
    return await crud.create(session, repo_model(**create_data))


async def get(session: _AS, **filter_data) -> JsonType:
    """
    После успешного возврата «секрета»:
    \n  * При первом запросе по secret_key необходимо вернуть ранее сохранённый «секрет».
    \n  * После успешного получения «секрета» повторный запрос по тому же secret_key не должен выдавать конфиденциальные данные.
    \n  * Сохранить в логе (PostgreSQL) факт выдачи секрета (время, IP-адрес и т. д.).
    """
    return await crud.delete(session, repo_model, **filter_data)


async def delete(session: _AS, passphrase: str | None, **filter_data) -> JsonType:
    """
    Может потребоваться, если при создании секрета передавался passphrase (или по иной логике, если это предусмотрено бизнес-требованиями).
    После успешного удаления:
    \n  * Сервис должен сделать секрет недоступным даже при первом запросе
    \n  * Сохранить в логе (PostgreSQL) факт удаления (ключ секрета, время, IP-адрес, метаданные о passphrase и т. д.).
    """
    assert session.in_transaction()
    obj = await crud.get_one(session, repo_model, **filter_data)
    if obj.passphrase != passphrase:
        return None
    return await crud.delete(session, repo_model, **filter_data)


# If you don't use an alembic -> uncomment below
# async def create_db_and_tables() -> None:
#     await crud.create_db_and_tables()
