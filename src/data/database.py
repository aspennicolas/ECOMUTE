from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# SQLite database file will be created in your project root
DATABASE_URL = "sqlite+aiosqlite:///./ecomute.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a DB session per request."""
    async with AsyncSessionLocal() as session:
        yield session