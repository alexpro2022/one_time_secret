# https://docs.pydantic.dev/
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from src.types_app import TypePK


class Base(BaseModel):
    # https://docs.pydantic.dev/2.2/usage/model_config
    model_config = ConfigDict(
        # extra="ignore",  # default behaviour
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        hide_input_in_errors=True,
    )
    id: TypePK | None = None

    @staticmethod
    def parse(exception: ValidationError):
        return " -> ".join(map(str.strip, str(exception).split("\n")[:-1]))

    @classmethod
    def is_valid(cls, **data) -> tuple[bool, Any]:
        try:
            return True, cls.model_validate(data)
        except ValidationError as e:
            return False, cls.parse(e)
