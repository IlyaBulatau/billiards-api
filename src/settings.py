from functools import cached_property

from config.common import Configuration, ConfigurationBuilder
from config.env import EnvVars
from pydantic import BaseModel


ENV_VAR_PREFIX = "APP_"


class S3Storage(BaseModel):
    access_key: str
    secret_key: str
    endpoint: str
    bucket: str


class Database(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str
    overflow: int = 100
    pool_size: int = 30
    pool_timeout: int = 30
    echo: bool = True

    @cached_property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )


class Settings(BaseModel):
    api_version: str
    show_error_details: bool
    api_default_page_size: int = 100
    api_max_page_size: int = 1000
    database: Database
    s3: S3Storage


def default_configuration_builder() -> ConfigurationBuilder:
    builder = ConfigurationBuilder(EnvVars(ENV_VAR_PREFIX))
    return builder


def default_configuration() -> Configuration:
    builder = default_configuration_builder()
    return builder.build()


def load_settings() -> Settings:
    config_root = default_configuration()
    return config_root.bind(Settings)


settings = load_settings()
