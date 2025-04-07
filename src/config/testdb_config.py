from src.config.base import (  # , model_validator
    BaseDBConf,
    NullPool,
    SettingsConfigDict,
)


class SettingsTestDB(BaseDBConf):
    model_config = SettingsConfigDict(env_prefix="TEST_")

    DEFAULT = "github_actions"

    # DEFAULT_FOR_GH_ACTIONS: str = "github_actions"
    # DEFAULT: str = DEFAULT_FOR_GH_ACTIONS

    # @model_validator(mode="after")
    # def check_attrs(self) -> "SettingsTestDB":
    #     super().check_attrs()
    #     if self.DEFAULT == self.DEFAULT_FOR_GH_ACTIONS:
    #         self.DB_HOST = "0.0.0.0"
    #     return self


db_conf = SettingsTestDB()
engine, async_session, get_async_session = db_conf.get_async_engine_session(
    poolclass=NullPool,
    # expire_on_commit=False,
    # autoflush=False,
)
