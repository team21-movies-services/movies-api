from pydantic import BaseSettings

ENV_FILE = ".env"


class TestSettings(BaseSettings):
    class Config:
        env_file = ENV_FILE

    redis_host: str
    redis_port: int

    elastic_host: str
    elastic_port: int
    es_id_field: str = "uuid"
    service_url: str = "http://api:8000/api/v1/"


test_settings = TestSettings()
