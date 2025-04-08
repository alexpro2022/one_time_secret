from collections.abc import Callable
from typing import Annotated, Any, TypeAlias, TypeVar

from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.repo.models.base import Base, TypeModel, TypePK  # noqa

_F = TypeVar("_F", bound=Callable[..., Any])
_TM = TypeVar("_TM")  # , bound=TypeModel)
_AS = TypeVar("_AS", bound=AsyncSession)
_ASM = TypeVar("_ASM", bound=async_sessionmaker)

JsonType: TypeAlias = dict[str, str]
DictType: TypeAlias = dict[str, Any]
NonEmptyStr = Annotated[str, Field(min_length=1, max_length=5000)]

# TESTS ====================
TypeFieldsListNone: TypeAlias = list[str] | None
TypeFieldsDict: TypeAlias = dict[str, Any]
TypeResponseJson: TypeAlias = dict | list | None
