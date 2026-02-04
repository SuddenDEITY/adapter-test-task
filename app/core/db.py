from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.interfaces import DatabaseManagerProtocol
from app.core.settings import Settings


class DatabaseManager:
    def __init__(self, settings: Settings) -> None:
        self._engine: AsyncEngine = create_async_engine(
            str(settings.postgres_dsn),
            echo=settings.postgres_echo,
            pool_size=settings.postgres_pool_size,
            max_overflow=settings.postgres_max_overflow,
            pool_recycle=settings.postgres_pool_recycle,
            pool_timeout=settings.postgres_pool_timeout,
            pool_pre_ping=settings.postgres_pool_pre_ping,
        )
        self._sessionmaker = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    async def connect(self) -> None:
        async with self._engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

    async def dispose(self) -> None:
        await self._engine.dispose()

    def session(self) -> AsyncSession:
        return self._sessionmaker()


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    manager: DatabaseManagerProtocol = request.app.state.db
    async with manager.session() as session:
        yield session
