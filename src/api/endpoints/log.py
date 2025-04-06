from fastapi import APIRouter

from src.api.dependencies import async_session
from src.config.app_config import app_conf
from src.models.log import Log
from src.repo.db import crud

router = APIRouter(prefix=f"{app_conf.url_prefix}/log", tags=["Logs"])


@router.get("")
async def get_logs(session: async_session):
    return await crud.get_all(session, Log)
