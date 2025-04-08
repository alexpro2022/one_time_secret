from datetime import datetime as dt

from src.api.schemas.base import Base, TypePK
from src.models.events import Event


class Log(Base):
    client_info: str
    secret_id: TypePK
    event: Event
    event_time: dt
