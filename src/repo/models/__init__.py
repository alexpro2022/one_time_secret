"""Import all your models here. It is necssary for the alembic migrations."""

from src.repo.models.base import Base  # noqa

# Below is for example
from src.models.secret import Secret  # noqa
