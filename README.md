# Core

## Контекст и цели
Этот репозиторий содержит core-модуль для FastAPI-приложения. Core предоставляет единые интерфейсы
доступа к PostgreSQL и Redis, а также управление жизненным циклом подключений.

## Ключевые решения
- Разделение ответственности: настройки, менеджеры БД/Redis, DI и lifespan вынесены в отдельные модули.
- Dependency Injection: доступ к `AsyncSession` и `Redis` через зависимости FastAPI.
- Lifespan: инициализация/освобождение ресурсов при старте/остановке приложения.
- Настройки: Pydantic Settings с `.env` и валидацией типов.

## Структура
```
app/
  main.py
  __main__.py
  core/
    __init__.py
    settings.py
    interfaces.py
    db.py
    redis.py
    lifespan.py
```

## Запуск
1. Поднять сервисы:
```
docker compose up -d
```
2. Установить зависимости:
```
poetry install
```
3. Запустить приложение:
```
poetry run python -m app
```

Проверка:
```
curl http://localhost:8000/health
```

## Использование core модуля
- `get_db_session` — получить `AsyncSession` для запросов в PostgreSQL.
- `get_redis_client` — получить `Redis` клиент.
- `Settings` — единый источник конфигурации.

## Тесты
```
poetry install --with dev
poetry run pytest
```
