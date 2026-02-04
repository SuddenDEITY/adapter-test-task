from typing import AsyncGenerator

from fastapi import Request
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from app.core.interfaces import RedisManagerProtocol
from app.core.settings import Settings


class RedisManager:
    def __init__(self, settings: Settings) -> None:
        self._pool = ConnectionPool.from_url(
            settings.redis_url,
            decode_responses=settings.redis_decode_responses,
            socket_timeout=settings.redis_socket_timeout,
            socket_connect_timeout=settings.redis_socket_connect_timeout,
        )
        self._redis = Redis(connection_pool=self._pool)

    async def connect(self) -> None:
        await self._redis.ping()

    async def close(self) -> None:
        await self._redis.close()
        await self._pool.disconnect()

    def client(self) -> Redis:
        return self._redis


async def get_redis_client(request: Request) -> AsyncGenerator[Redis, None]:
    manager: RedisManagerProtocol = request.app.state.redis
    yield manager.client()
