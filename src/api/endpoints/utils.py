from collections.abc import Coroutine
from typing import Any

from fastapi import HTTPException, status
from src.repo.db.exceptions import NotFound


async def try_return(
    return_coro: Coroutine,
    possible_exception=NotFound,
    raise_status_code: int = status.HTTP_404_NOT_FOUND,
) -> Any:
    try:
        return await return_coro
    except possible_exception as e:
        raise HTTPException(status_code=raise_status_code, detail=e.msg)
