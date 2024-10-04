import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DB_URL, echo=bool(os.getenv('DEBUG', False)))


async def async_session_generator() -> AsyncGenerator[AsyncSession, None]:
    session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with session_maker() as session:
        yield session
