from datetime import datetime as dt
from typing import Annotated

from fastapi import BackgroundTasks, Depends

from src.api.dependencies import async_session, client_info
from src.models.log import Event
from src.repo.db import crud
from src.repo.models import Secret
from src.services.log import logger
from src.types_app import TypeModel


class SecretService:
    model = Secret

    def __init__(
        self,
        client_info: client_info,
        session: async_session,
        bg_tasks: BackgroundTasks,
    ):
        self.client_info = ":".join(map(str, client_info.values()))
        self.session = session
        self.bg_tasks = bg_tasks

    async def create(self, **create_data) -> TypeModel:
        """
        После успешного создания секрета сервис должен:
        \n  * Сохранить секрет.
        \n  * Залогировать создание секрета в PostgreSQL (например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.).
        """
        assert self.session.in_transaction()
        # encode in schema
        scrt = await crud.create(self.session, self.model(**create_data))
        self.bg_tasks.add_task(
            logger, self.client_info, scrt.id, Event.created, dt.now()
        )
        # self.bg_tasks.add_task(cache.set(scrt, expire=ttl_seconds))
        # task db delete on ttl expire
        return scrt

    async def delete(
        self, passphrase: str | None = None, checkpass: bool = True, **filter_data
    ) -> TypeModel | None:
        """
        Может потребоваться, если при создании секрета передавался passphrase (или по иной логике, если это предусмотрено бизнес-требованиями).
        После успешного удаления:
        \n  * Сервис должен сделать секрет недоступным даже при первом запросе
        \n  * Сохранить в логе (PostgreSQL) факт удаления (ключ секрета, время, IP-адрес, метаданные о passphrase и т. д.).
        """
        assert self.session.in_transaction()
        if checkpass:
            scrt = await crud.get_one(self.session, self.model, **filter_data)
            if scrt.passphrase != passphrase:
                return None
        scrt = await crud.delete(self.session, self.model, **filter_data)
        self.bg_tasks.add_task(
            logger, self.client_info, scrt.id, Event.deleted, dt.now()
        )
        # self.bg_tasks.add_task(cache.delete(scrt, expire=ttl_seconds))
        return scrt

    async def get(self, **filter_data):
        """
        После успешного возврата «секрета»:
        \n  * При первом запросе по secret_key необходимо вернуть ранее сохранённый «секрет».
        \n  * После успешного получения «секрета» повторный запрос по тому же secret_key не должен выдавать конфиденциальные данные.
        \n  * Сохранить в логе (PostgreSQL) факт выдачи секрета (время, IP-адрес и т. д.).
        """
        assert self.session.in_transaction()
        # scrt = cache.get(**filter_data)
        # if scrt
        # yield scrt
        self.bg_tasks.add_task(
            logger, self.client_info, filter_data["id"], Event.read, dt.now()
        )
        yield await self.delete(checkpass=False, **filter_data)
        # decode in schema


secret_service = Annotated[SecretService, Depends()]
