from toolkit.repo.db import crud

from src.config import db_config as c
from src.models import Log


async def logger(client_info, secret_id, event, event_time) -> None:
    async with c.async_session.begin() as session:
        await crud.create(
            session,
            Log(
                client_info=client_info,
                secret_id=secret_id,
                event=event,
                event_time=event_time,
            ),
        )
