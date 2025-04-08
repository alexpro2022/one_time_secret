from src.config.base import BaseDBConf, SettingsConfigDict


class SettingsDB(BaseDBConf):
    model_config = SettingsConfigDict(env_prefix="DB_")


db_conf = SettingsDB()

engine, async_session, get_async_session = db_conf.get_dependencies(
    echo=True,
    # expire_on_commit=False,
    # autoflush=False,
)
