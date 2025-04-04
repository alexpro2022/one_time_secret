from pydantic import EmailStr, SecretStr

from src.config.base import BaseConf


class SettingsApp(BaseConf):
    # Below settings are mostly for FastAPI/FastAPI_Users
    URL_PREFIX: str = "/api/v1"
    DEFAULT_STR: str = "To be implemented in .env file"
    SUPER_ONLY: str = "__Только для суперюзеров:__ "
    AUTH_ONLY: str = "__Только для авторизованных пользователей:__ "
    ALL_USERS: str = "__Для всех пользователей:__ "

    app_title: str = f"App title {DEFAULT_STR}"
    app_description: str = f"App description {DEFAULT_STR}"
    # secret_key: SecretStr = f"Secret key {DEFAULT_STR}"
    secret_min_ttl: int = 0

    # authentication
    admin_email: EmailStr = "adm@adm.com"
    admin_password: str = "adm"
    password_length: int = 3
    auth_backend_name: str = "jwt"
    token_url: str = "auth/jwt/login"
    token_lifetime: int = 3600


app_conf = SettingsApp()
