from enum import Enum


class Event(Enum):
    created: str = "created"
    read: str = "read"
    deleted: str = "deleted"
