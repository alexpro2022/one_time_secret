# from src.repo.db import crud
from src.types_app import _AS, TypeModel, TypePK


async def create(session: _AS, model: TypeModel, **create_data) -> TypeModel:
    """
    После успешного создания секрета сервис должен:
    \n  * Сохранить секрет.
    \n  * Залогировать создание секрета в PostgreSQL (например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.).
    """
    assert session.in_transaction()
    # return await crud.create(session, model(**create_data))
    return {"secret_key": "уникальный_идентификатор"}


async def get(session: _AS, model: TypeModel, **filter_data) -> TypeModel:
    """
    После успешного возврата «секрета»:
    \n  * При первом запросе по secret_key необходимо вернуть ранее сохранённый «секрет».
    \n  * После успешного получения «секрета» повторный запрос по тому же secret_key не должен выдавать конфиденциальные данные.
    \n  * Сохранить в логе (PostgreSQL) факт выдачи секрета (время, IP-адрес и т. д.).
    """
    # return await crud.get_one(session, model, **filter_data)
    return {"secret": "доступ_к_конфиденциальным_данным"}


async def delete(session: _AS, model: TypeModel, id: TypePK) -> TypeModel:
    """
    Может потребоваться, если при создании секрета передавался passphrase (или по иной логике, если это предусмотрено бизнес-требованиями).
    После успешного удаления:
    \n  * Сервис должен сделать секрет недоступным даже при первом запросе
    \n  * Сохранить в логе (PostgreSQL) факт удаления (ключ секрета, время, IP-адрес, метаданные о passphrase и т. д.).
    """
    assert session.in_transaction()
    # return await crud.delete(session, model, id)
    return {"status": "secret_deleted"}


# If you don't use an alembic -> uncomment below
# async def create_db_and_tables() -> None:
#     await crud.create_db_and_tables()
