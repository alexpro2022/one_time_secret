from collections.abc import Callable
from typing import Annotated, Any, TypeAlias, TypeVar

from fastapi import Depends
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config.db_config import get_async_session
from src.repo.models.base import Base, TypeModel, TypePK  # noqa

# Common types ===============================================
_F = TypeVar("_F", bound=Callable[..., Any])
# _EXCEPTION = TypeVar("_EXCEPTION", bound=[Exception | list[Exception]])

# Repo types ===============================================
# TypeModel = TypeVar("TypeModel", bound=Base)
# _TM = TypeVar("_TM", bound=Base)
_TM = TypeVar("_TM")  # , bound=TypeModel)
_AS = TypeVar("_AS", bound=AsyncSession)
_ASM = TypeVar("_ASM", bound=async_sessionmaker)
# _AS: TypeAlias = AsyncSession

# example from pydantic
# AnyClassMethod = classmethod[Any, Any, Any]
# TupleGenerator = typing.Generator[typing.Tuple[str, Any], None, None]
# Model = typing.TypeVar('Model', bound='BaseModel')
# @classmethod
# def model_validate(
#     cls: type[Model],

# FastAPI types ===============================================
# from typing import Annotated
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends
# from src.config.db_config import get_async_session

async_session = Annotated[AsyncSession, Depends(get_async_session)]
StrFieldType = Annotated[str, Field(min_length=1)]
PositiveInt = Annotated[int, Field(default=1, gt=0)]
JsonType: TypeAlias = dict[str, str]


# Bot types ===============================================
# from typing import TypeAlias
# from aiogram.types import CallbackQuery, Message


# TESTS ====================
TypeFieldsListNone: TypeAlias = list[str] | None
TypeFieldsDict: TypeAlias = dict[str, Any]
TypeResponseJson: TypeAlias = dict | list | None
# dict[str, Any] | None = None
