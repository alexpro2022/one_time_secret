from typing import Any, TypeAlias

from fastapi import status
from pydantic import BaseModel

ResponseType: TypeAlias = dict[int, dict[BaseModel, Any]]


def _response(status_code: int, message: str, description: Any) -> ResponseType:
    class Message(BaseModel):
        detail: str = message

    return {status_code: {"model": Message, "description": description}}


def response_400(name: str) -> ResponseType:
    return _response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=f"{name} already exists",
        description="The item already exists",
    )


def response_404(name: str) -> ResponseType:
    return _response(
        status_code=status.HTTP_404_NOT_FOUND,
        message=f"{name} not found",
        description="The item was not found",
    )
