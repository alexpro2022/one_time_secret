from src.repo.models.base import Base, Mapped, mapped_column


class Secret(Base):
    name: Mapped[str] = mapped_column(index=True, unique=True)
    secret_name: Mapped[str]
    age: Mapped[int | None]
    new_field: Mapped[str] = mapped_column(default="To update manually")
