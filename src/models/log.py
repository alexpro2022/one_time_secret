from datetime import datetime

from src.models.events import Event
from src.repo.models.base import Base, Mapped, TypePK, mapped_column
from src.utils import get_time_now


class Log(Base):
    """Лог событий (например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.)."""

    client_info: Mapped[str]
    secret_id: Mapped[TypePK]
    event: Mapped[Event]
    event_time: Mapped[datetime] = mapped_column(default=get_time_now)
