all = [
    "async_create_table",
    "async_session"
]

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base

# Создаём асинхронный движок (SQLite через aiosqlite)
engine = create_async_engine("sqlite+aiosqlite:///instance/sqlite.db", echo=False)

# Фабрика сессий
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Создание таблиц
async def async_create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)