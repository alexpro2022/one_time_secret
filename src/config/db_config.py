from src.config.base import BaseDBConf


class SettingsDB(BaseDBConf):
    pass


db_conf = SettingsDB()
engine, async_session, get_async_session = db_conf.get_async_engine_session(
    echo=True,
    # expire_on_commit=False,
    # autoflush=False,
)


# assert (
#     str(db_conf.DATABASE_URI)
#     == "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"
# )
