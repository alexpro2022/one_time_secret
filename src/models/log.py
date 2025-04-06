from datetime import datetime as dt
from enum import Enum

from src.config.base import NonEmptyStr
from src.repo.models.base import Base, Mapped, mapped_column
from src.types_app import TypePK


class Event(Enum):
    created: NonEmptyStr = "created"
    read: NonEmptyStr = "read"
    deleted: NonEmptyStr = "deleted"


class Log(Base):
    """(например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.)."""

    client_info: Mapped[str]
    secret_id: Mapped[TypePK]
    event: Mapped[Event]
    event_time: Mapped[dt] = mapped_column(default=dt.now)
