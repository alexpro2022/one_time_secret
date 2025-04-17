from datetime import datetime

from toolkit.schemas.base import Base, TypePK

from src.models.utils import Event


class Log(Base):
    client_info: str
    secret_id: TypePK
    event: Event
    event_time: datetime
