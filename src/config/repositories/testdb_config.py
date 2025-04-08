from src.config.base import BaseDBConf, NullPool, SettingsConfigDict


class SettingsTestDB(BaseDBConf):
    model_config = SettingsConfigDict(env_prefix="TEST_DB_")


db_conf = SettingsTestDB()

engine, async_session, get_async_session = db_conf.get_dependencies(
    poolclass=NullPool,
    # expire_on_commit=False,
    # autoflush=False,
)
