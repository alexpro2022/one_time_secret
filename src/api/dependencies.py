from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.utils import get_client_info, set_headers_no_client_cache
from src.config.db_config import get_async_session

async_session = Annotated[AsyncSession, Depends(get_async_session)]
client_info = Annotated[dict[str, Any], Depends(get_client_info)]
set_headers = Depends(set_headers_no_client_cache)

from src.services.secret import SecretService  # noqa

secret_service = Annotated[SecretService, Depends()]
