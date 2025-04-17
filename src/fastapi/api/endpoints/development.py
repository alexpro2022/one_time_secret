"""
The endpoints are not a part of the project.
They are just for convenient checking on development.
"""

from toolkit.api.fastapi.dependencies import async_session
from toolkit.repo.db import crud

from fastapi import APIRouter
from src.config import app_config as c
from src.models import Log, Secret

router = APIRouter(
    prefix=f"{c.app_conf.url_prefix}/development",
    tags=["Development"],
)


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
