from src.repo.models.base import Base, Mapped, mapped_column


class Secret(Base):
    secret: Mapped[str]  # = mapped_column(index=True, unique=True)
    passphrase: Mapped[str | None]
    ttl_seconds: Mapped[int | None]
