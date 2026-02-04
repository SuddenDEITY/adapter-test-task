from functools import lru_cache
from typing import Optional

from fastapi import Request
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )

    app_name: str = Field(
        default="test-service",
        alias="APP_NAME",
        description="Application name for metadata and logging.",
    )
    app_host: str = Field(
        default="0.0.0.0",
        alias="APP_HOST",
        description="Host for running the web server.",
    )
    app_port: int = Field(
        default=8002,
        alias="APP_PORT",
        description="Port for running the web server.",
    )
    log_level: str = Field(
        default="info",
        alias="LOG_LEVEL",
        description="Logging level for the application.",
    )

    postgres_dsn: PostgresDsn = Field(
        alias="POSTGRES_DSN",
        description="PostgreSQL DSN for async SQLAlchemy engine.",
    )
    postgres_echo: bool = Field(
        default=False,
        alias="POSTGRES_ECHO",
        description="Enable SQLAlchemy SQL echo logging.",
    )
    postgres_pool_size: int = Field(
        default=5,
        alias="POSTGRES_POOL_SIZE",
        description="Size of the connection pool.",
    )
    postgres_max_overflow: int = Field(
        default=10,
        alias="POSTGRES_MAX_OVERFLOW",
        description="Maximum number of overflow connections.",
    )
    postgres_pool_recycle: int = Field(
        default=1800,
        alias="POSTGRES_POOL_RECYCLE",
        description="Seconds after which a connection is recycled.",
    )
    postgres_pool_timeout: int = Field(
        default=30,
        alias="POSTGRES_POOL_TIMEOUT",
        description="Seconds to wait for a connection before timing out.",
    )
    postgres_pool_pre_ping: bool = Field(
        default=True,
        alias="POSTGRES_POOL_PRE_PING",
        description="Enable SQLAlchemy pool pre-ping.",
    )

    redis_url: str = Field(
        alias="REDIS_URL",
        description="Redis connection URL.",
    )
    redis_decode_responses: bool = Field(
        default=True,
        alias="REDIS_DECODE_RESPONSES",
        description="Decode Redis responses to strings.",
    )
    redis_socket_timeout: int = Field(
        default=5,
        alias="REDIS_SOCKET_TIMEOUT",
        description="Redis socket timeout in seconds.",
    )
    redis_socket_connect_timeout: int = Field(
        default=5,
        alias="REDIS_SOCKET_CONNECT_TIMEOUT",
        description="Redis socket connect timeout in seconds.",
    )


@lru_cache(maxsize=1)
def _cached_settings() -> Settings:
    return Settings()


def get_settings(request: Optional[Request] = None) -> Settings:
    if request is not None:
        return request.app.state.settings
    return _cached_settings()
