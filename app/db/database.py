from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core import config

DATABASE_URL = f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASS}@{config.POSTGRES_HOST}/{config.POSTGRES_DB_NAME}"

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a session factory bound to the async engine
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevents issues with accessing attributes after commit
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()  # Explicitly close the session
