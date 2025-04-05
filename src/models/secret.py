from src.repo.models.base import Base, Mapped


class Secret(Base):
    secret: Mapped[str]
    passphrase: Mapped[str | None]
    ttl_seconds: Mapped[int | None]
