from fastapi import BackgroundTasks

from src.repo.db import crud
from src.repo.models import Secret
from src.types_app import _AS, DictType, TypeModel


async def create(
    client_info: DictType,
    session: _AS,
    bg_tasks: BackgroundTasks,
    **create_data,
) -> TypeModel:
    """
    После успешного создания секрета сервис должен:
    \n  * Сохранить секрет.
    \n  * Залогировать создание секрета в PostgreSQL (например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.).
    """
    assert session.in_transaction()
    # encode
    scrt = await crud.create(session, Secret(**create_data))
    # if sqrt:
    #   log
    # cache ttl expire
    # task db delete on ttl expire
    return scrt


async def get(
    client_info: DictType,
    session: _AS,
    bg_tasks: BackgroundTasks,
    **filter_data,
) -> TypeModel:
    """
    После успешного возврата «секрета»:
    \n  * При первом запросе по secret_key необходимо вернуть ранее сохранённый «секрет».
    \n  * После успешного получения «секрета» повторный запрос по тому же secret_key не должен выдавать конфиденциальные данные.
    \n  * Сохранить в логе (PostgreSQL) факт выдачи секрета (время, IP-адрес и т. д.).
    """
    assert session.in_transaction()
    # assert 0, client_info
    # scrt = await cache.delete
    scrt = await crud.delete(session, Secret, **filter_data)
    # decode
    # log
    return scrt


async def delete(
    client_info: DictType,
    session: _AS,
    bg_tasks: BackgroundTasks,
    passphrase: str | None,
    **filter_data,
) -> TypeModel | None:
    """
    Может потребоваться, если при создании секрета передавался passphrase (или по иной логике, если это предусмотрено бизнес-требованиями).
    После успешного удаления:
    \n  * Сервис должен сделать секрет недоступным даже при первом запросе
    \n  * Сохранить в логе (PostgreSQL) факт удаления (ключ секрета, время, IP-адрес, метаданные о passphrase и т. д.).
    """
    assert session.in_transaction()
    obj = await crud.get_one(session, Secret, **filter_data)
    if obj.passphrase != passphrase:
        return None
    return await crud.delete(session, Secret, **filter_data)
