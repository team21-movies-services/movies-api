import os
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings, Field

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

ENV_FILE = ".env"


class Settings(BaseSettings):
    """Настройки проекта."""

    class Config:
        env_file = ENV_FILE

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # PROJECT
    project_name: str = "movies"
    cache_expire: int = 300  # 5 минут

    # REDIS
    redis_host: str = "redis"
    redis_port: int = 6379

    # ELASTICSEARCH
    elastic_host: str = "elasticsearch"
    elastic_port: int = 9200

    jwt_secret_key: str = Field(default=...)


@lru_cache()
def get_settings():
    return Settings()


config = get_settings()
