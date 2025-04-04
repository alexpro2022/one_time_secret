from src.config.base import BaseDBConf, NullPool, SettingsConfigDict, model_validator


class SettingsTestDB(BaseDBConf):
    # model_config = {**BaseDBConf.model_config, **{"env_prefix": "TEST_"}}
    model_config = SettingsConfigDict(env_prefix="TEST_")

    DEFAULT_FOR_GH_ACTIONS: str = "github_actions"
    DEFAULT: str = DEFAULT_FOR_GH_ACTIONS

    @model_validator(mode="after")
    def check_attrs(self) -> "SettingsTestDB":
        super().check_attrs()
        if self.DEFAULT == self.DEFAULT_FOR_GH_ACTIONS:
            self.DB_HOST = "0.0.0.0"
        return self


db_conf = SettingsTestDB()
engine, async_session, get_async_session = db_conf.get_async_engine_session(
    poolclass=NullPool,
    # expire_on_commit=False,
    # autoflush=False,
)


# assert (
#     str(test_db_conf.DATABASE_URI)
#     == "postgresql+asyncpg://postgres_test_user:postgres_test_pwd@postgres_test_host:5432/postgres_test_name"
#     # == "postgresql+asyncpg://github_actions:github_actions@0.0.0.0:5432/github_actions"
# )
