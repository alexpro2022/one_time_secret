from src.config.base import BaseConf, PositiveInt, SecretStr


class SettingsApp(BaseConf):
    DEFAULT_STR: str = "To be implemented in .env file"
    url_prefix: str = "/api/v1"
    app_title: str = f"App title: {DEFAULT_STR}"
    app_description: str = f"App description: {DEFAULT_STR}"
    secret_min_ttl: PositiveInt = 5 * 60
    secret_key: SecretStr = "wxvQEAtuRjtCHpeL9VPvy7SLVAQHZhlp-Pswcp7RCyw="


app_conf = SettingsApp()
