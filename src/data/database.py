from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# SQLite database file will be created in your project root
DATABASE_URL = "sqlite+aiosqlite:///./ecomute.db"

# The engine is the low-level connection to the database.
# echo=True prints every SQL statement to the console — useful for debugging.
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# A session factory: calling AsyncSessionLocal() gives us a new DB session.
# expire_on_commit=False keeps ORM objects usable after a commit (important for async).
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a DB session per request.

    Used with Depends(get_db) in routers/datasources. FastAPI calls this
    generator, injects the session, and closes it automatically when the
    request finishes (the 'async with' handles cleanup).
    """
    async with AsyncSessionLocal() as session:
        yield session