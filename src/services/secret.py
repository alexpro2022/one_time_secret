from typing import Annotated

from fastapi import BackgroundTasks, Depends

from src.api.dependencies import async_session, client_info
from src.repo.db import crud
from src.repo.models import Secret
from src.types_app import TypeModel


class SecretService:
    def __init__(
        self,
        client_info: client_info,
        session: async_session,
        bg_tasks: BackgroundTasks,
    ):
        self.client_info = client_info
        self.session = session
        self.bg_tasks = bg_tasks
        self.model = Secret

    async def create(self, **create_data) -> TypeModel:
        """
        После успешного создания секрета сервис должен:
        \n  * Сохранить секрет.
        \n  * Залогировать создание секрета в PostgreSQL (например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.).
        """
        assert self.session.in_transaction()
        # encode
        scrt = await crud.create(self.session, self.model(**create_data))
        # if sqrt:
        #   log
        # cache ttl expire
        # task db delete on ttl expire
        return scrt

    async def get(self, **filter_data) -> TypeModel:
        """
        После успешного возврата «секрета»:
        \n  * При первом запросе по secret_key необходимо вернуть ранее сохранённый «секрет».
        \n  * После успешного получения «секрета» повторный запрос по тому же secret_key не должен выдавать конфиденциальные данные.
        \n  * Сохранить в логе (PostgreSQL) факт выдачи секрета (время, IP-адрес и т. д.).
        """
        assert self.session.in_transaction()
        # assert 0, client_info
        # scrt = await cache.delete
        scrt = await crud.delete(self.session, self.model, **filter_data)
        # decode
        # log
        return scrt

    async def delete(self, passphrase: str | None, **filter_data) -> TypeModel | None:
        """
        Может потребоваться, если при создании секрета передавался passphrase (или по иной логике, если это предусмотрено бизнес-требованиями).
        После успешного удаления:
        \n  * Сервис должен сделать секрет недоступным даже при первом запросе
        \n  * Сохранить в логе (PostgreSQL) факт удаления (ключ секрета, время, IP-адрес, метаданные о passphrase и т. д.).
        """
        assert self.session.in_transaction()
        obj = await crud.get_one(self.session, self.model, **filter_data)
        if obj.passphrase != passphrase:
            return None
        return await crud.delete(self.session, self.model, **filter_data)


secret_service = Annotated[SecretService, Depends()]
