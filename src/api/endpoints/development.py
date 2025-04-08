from fastapi import APIRouter

from src.api.dependencies import async_session
from src.config.app_config import app_conf
from src.models.log import Log
from src.models.secret import Secret
from src.repo.db import crud

router = APIRouter(prefix=f"{app_conf.url_prefix}/development", tags=["Development"])


@router.get(
    "/logs",
    summary="All log records.",
    description="The endpoint is just for convenient log checking on development.",
)
async def get_logs(session: async_session):
    return await crud.get_all(session, Log)


@router.get(
    "/secrets",
    summary="All secret records.",
    description="The endpoint is just for convenient secret checking on development.",
)
async def get_secrets(session: async_session):
    return await crud.get_all(session, Secret)
