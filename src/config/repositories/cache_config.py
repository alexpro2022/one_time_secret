from src.config.base import BaseRedisConf, SettingsConfigDict


class SettingsRedis(BaseRedisConf):
    model_config = SettingsConfigDict(env_prefix="REDIS_")


redis_conf = SettingsRedis()
get_aioredis, _ = redis_conf.get_dependencies()
