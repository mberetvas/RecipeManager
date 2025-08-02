from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    "sqlite+aiosqlite:///.Database/RecipeManager.db",
    echo=True,  # Optional: for SQL logging
    future=True,
)


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Example usage:
"""
async def get_users():
    async with async_session() as session:
        result = await session.execute("SELECT * FROM users")
        users = result.fetchall()
        return users
"""
