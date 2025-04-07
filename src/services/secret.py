from datetime import datetime as dt

from fastapi import BackgroundTasks

from src.api.dependencies import async_session, client_info, redis
from src.models.events import Event
from src.models.secret import Secret
from src.repo.cache import crud as cache_crud
from src.repo.db import crud as db_crud
from src.services.log import logger
from src.types_app import TypeModel, TypePK


class SecretService:
    model = Secret

    def __init__(
        self,
        client_info: client_info,
        session: async_session,
        redis: redis,
        bg_tasks: BackgroundTasks,
    ):
        self.client_info = ":".join(map(str, client_info.values()))
        self.session = session
        self.redis = redis
        self.bg_tasks = bg_tasks

    async def _del(self, session=None, **filter_data):
        async def _():
            secret_id = filter_data["id"]
            self.bg_tasks.add_task(
                cache_crud.delete, client=self.redis, name=str(secret_id)
            )
            self.bg_tasks.add_task(
                logger, self.client_info, secret_id, Event.deleted, dt.now()
            )
            return await db_crud.delete(session, self.model, **filter_data)

        if session is None:
            from src.config.db_config import async_session

            async with async_session.begin() as session:
                return await _()
        return await _()

    async def get(self, **filter_data):
        """
        После успешного возврата «секрета»:
        \n  * При первом запросе по secret_key необходимо вернуть ранее сохранённый «секрет».
        \n  * После успешного получения «секрета» повторный запрос по тому же secret_key не должен выдавать конфиденциальные данные.
        \n  * Сохранить в логе (PostgreSQL) факт выдачи секрета (время, IP-адрес и т. д.).
        """
        assert self.session.in_transaction()
        self.bg_tasks.add_task(
            logger, self.client_info, filter_data["id"], Event.read, dt.now()
        )
        data = await cache_crud.get(self.redis, str(filter_data["id"]))
        if data:
            self.bg_tasks.add_task(self._del, **filter_data)
            return self.model(**data)
        return await self._del(self.session, **filter_data)

    async def delete(
        self, passphrase: str | None = None, **filter_data
    ) -> TypeModel | None:
        """
        Может потребоваться, если при создании секрета передавался passphrase (или по иной логике, если это предусмотрено бизнес-требованиями).
        После успешного удаления:
        \n  * Сервис должен сделать секрет недоступным даже при первом запросе
        \n  * Сохранить в логе (PostgreSQL) факт удаления (ключ секрета, время, IP-адрес, метаданные о passphrase и т. д.).
        """
        assert self.session.in_transaction()
        scrt = await db_crud.get_one(self.session, self.model, **filter_data)
        if scrt.passphrase != passphrase:
            return None
        return await self._del(self.session, **filter_data)

    async def create(self, **create_data) -> TypeModel:
        """
        После успешного создания секрета сервис должен:
        \n  * Сохранить секрет.
        \n  * Залогировать создание секрета в PostgreSQL (например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.).
        """
        assert self.session.in_transaction()
        scrt = await db_crud.create(self.session, self.model(**create_data))
        self.bg_tasks.add_task(
            logger, self.client_info, scrt.id, Event.created, dt.now()
        )
        self.bg_tasks.add_task(
            cache_crud.set,
            client=self.redis,
            name=str(scrt.id),
            value=scrt.model_dump("id"),  # type: ignore [arg-type]
            ex=scrt.ttl_seconds,
        )
        # task db delete on ttl expire
        # self.bg_tasks.add_task(
        #     self.set_expire, scrt.id, scrt.ttl_seconds
        # )
        return scrt

    async def set_expire(self, id: TypePK, delay: int) -> None:
        import asyncio

        await asyncio.sleep(delay)
        await self._del(id=id)
