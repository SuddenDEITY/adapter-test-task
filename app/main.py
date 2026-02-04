from fastapi import APIRouter, Depends, FastAPI
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import (
    Settings,
    create_lifespan,
    get_db_session,
    get_redis_client,
    get_settings,
)

router = APIRouter()


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title=settings.app_name, lifespan=create_lifespan(settings))
    app.include_router(router)
    return app


@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_client),
) -> dict:
    await db.execute(text("SELECT 1"))
    await redis.ping()
    return {"status": "ok"}
