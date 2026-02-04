import os
import uvicorn

from app.core.settings import get_settings


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:create_app",
        host=settings.app_host,
        port=settings.app_port,
        log_level=settings.log_level,
        factory=True,
        reload=os.getenv("APP_RELOAD", "false").lower() in {"1", "true", "yes", "on"},
    )
