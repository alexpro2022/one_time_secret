"""Import all your models here. It is necssary for the alembic migrations."""

from src.repo.models.base import Base  # noqa
from src.models.secret import Secret  # noqa
from src.models.log import Log  # noqa
