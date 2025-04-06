from datetime import datetime as dt

from src.models.events import Event
from src.repo.models.base import Base, Mapped, TypePK, mapped_column


class Log(Base):
    """(например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.)."""

    client_info: Mapped[str]
    secret_id: Mapped[TypePK]
    event: Mapped[Event]
    event_time: Mapped[dt] = mapped_column(default=dt.now)
