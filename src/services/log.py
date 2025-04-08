from src.config.repositories.db_config import async_session
from src.models.log import Log
from src.repo.db import crud


async def logger(client_info, secret_id, event, event_time) -> None:
    async with async_session.begin() as session:
        await crud.create(
            session,
            Log(
                client_info=client_info,
                secret_id=secret_id,
                event=event,
                event_time=event_time,
            ),
        )
