from pydantic import BaseSettings, Field

ENV_FILE = ".env"


class TestSettings(BaseSettings):
    class Config:
        env_file = ENV_FILE

    redis_host: str = Field(default=...)
    redis_port: int = Field(default=...)

    elastic_host: str = Field(default=...)
    elastic_port: int = Field(default=...)
    es_id_field: str = "uuid"
    service_url: str = "http://movies-api-test:8000/api/v1/"
    test_user_jwt: str = Field(default=...)


test_settings = TestSettings()
