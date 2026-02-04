from fastapi import Depends, FastAPI
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_settings, create_lifespan, get_db_session, get_redis_client, Settings


def create_app(settings: Settings) -> FastAPI:
    return FastAPI(title=settings.app_name, lifespan=create_lifespan(settings))

settings = get_settings()
app = create_app(settings)


@app.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_client),
) -> dict:
    await db.execute(text("SELECT 1"))
    await redis.ping()
    return {"status": "ok"}
