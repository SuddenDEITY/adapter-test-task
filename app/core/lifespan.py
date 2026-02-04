import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import DatabaseManager
from app.core.redis import RedisManager
from app.core.settings import Settings


def create_lifespan(settings: Settings):
    logger = logging.getLogger("app.lifespan")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.settings = settings
        app.state.db = DatabaseManager(settings)
        app.state.redis = RedisManager(settings)

        try:
            await app.state.db.connect()
            await app.state.redis.connect()
        except Exception:
            logger.exception("Failed to initialize resources")
            await app.state.redis.close()
            await app.state.db.dispose()
            raise

        yield

        await app.state.redis.close()
        await app.state.db.dispose()

    return lifespan
