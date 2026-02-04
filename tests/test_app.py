import types

import pytest

from app.core import get_db_session, get_redis_client
from app.core.settings import Settings
from app.main import create_app


@pytest.mark.asyncio
async def test_get_db_session_uses_app_state():
    class FakeDbManager:
        async def connect(self) -> None:
            return None

        async def dispose(self) -> None:
            return None

        def session(self):
            class _Session:
                async def __aenter__(self):
                    return "session"

                async def __aexit__(self, exc_type, exc, tb):
                    return None

            return _Session()

    app = create_app(
        Settings(
            postgres_dsn="postgresql+asyncpg://user:pass@localhost:5432/db",
            redis_url="redis://localhost:6379/0",
        )
    )
    app.state.db = FakeDbManager()

    request = types.SimpleNamespace(app=app)

    gen = get_db_session(request)
    session = await gen.__anext__()
    assert session == "session"
    await gen.aclose()


@pytest.mark.asyncio
async def test_get_redis_client_uses_app_state():
    class FakeRedisManager:
        async def connect(self) -> None:
            return None

        async def close(self) -> None:
            return None

        def client(self):
            return "redis-client"

    app = create_app(
        Settings(
            postgres_dsn="postgresql+asyncpg://user:pass@localhost:5432/db",
            redis_url="redis://localhost:6379/0",
        )
    )
    app.state.redis = FakeRedisManager()

    request = types.SimpleNamespace(app=app)

    gen = get_redis_client(request)
    client = await gen.__anext__()
    assert client == "redis-client"
    await gen.aclose()
