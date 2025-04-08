from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.utils import get_client_info, set_headers_no_client_cache
from src.config.base import aioredis
from src.config.repositories.cache_config import get_aioredis
from src.config.repositories.db_config import get_async_session

async_session = Annotated[AsyncSession, Depends(get_async_session)]
client_info = Annotated[dict[str, Any], Depends(get_client_info)]
set_headers = Depends(set_headers_no_client_cache)
redis = Annotated[aioredis.Redis, Depends(get_aioredis)]

from src.services.secret import SecretService  # noqa

secret_service = Annotated[SecretService, Depends()]
