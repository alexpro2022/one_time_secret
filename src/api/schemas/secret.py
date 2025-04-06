from pydantic import BaseModel, Field

from src.config.app_config import app_conf
from src.types_app import StrFieldType


class Secret(BaseModel):
    """
    Пример ответа (JSON):
    {
    "secret": "доступ_к_конфиденциальным_данным"
    }
    """

    secret: StrFieldType = Field(
        description="обязательный параметр, конфиденциальные данные.",
        examples=["доступ_к_конфиденциальным_данным"],
    )


class SecretCreate(Secret):
    """
    Тело POST-запроса (JSON) может содержать:
    * secret (string) — обязательный параметр, конфиденциальные данные.
    * passphrase (string) — опциональный параметр, фраза-пароль для дополнительной защиты (например, может потребоваться при удалении).
    * ttl_seconds (number) — опциональный параметр, время жизни секрета в секундах.

    Пример тела запроса:
    {
    "secret": "доступ_к_конфиденциальным_данным",
    "passphrase": "my_passphrase",
    "ttl_seconds": 3600
    }
    """

    passphrase: StrFieldType | None = Field(
        default=None,
        description="Опциональный параметр, фраза-пароль для дополнительной защиты (например, может потребоваться при удалении).",
        examples=["my_passphrase"],
    )
    ttl_seconds: int | None = Field(
        default=app_conf.secret_min_ttl,
        description="Опциональный параметр, время жизни секрета в секундах.",
        ge=app_conf.secret_min_ttl,
        examples=["300"],
    )


class SecretKey(BaseModel):
    """
    Пример ответа (JSON) на POST-запрос:
    {
    "secret_key": "уникальный_идентификатор"
    }
    """

    secret_key: str = Field(
        description="Уникальный_идентификатор секретных данных, например первичный ключ формата UUID.",
        examples=["уникальный_идентификатор"],
    )


class SecretDelete(BaseModel):
    """
    Пример ответа (JSON):
    {
    "status": "secret_deleted"
    }
    """

    status: str = Field(examples=["secret_deleted"])
