from datetime import datetime

from toolkit.models.base import Base, Mapped, TypePK, mapped_column
from toolkit.utils.utils import get_time_now

from src.models.utils import Event


class Log(Base):
    """Лог событий (например, ID секрета, время создания, IP-адрес, при необходимости — указание ttl_seconds и т. д.)."""

    client_info: Mapped[str]
    secret_id: Mapped[TypePK]
    event: Mapped[Event]
    event_time: Mapped[datetime] = mapped_column(default=get_time_now)
