import asyncio
from BackEnd.orm_models import Base
from BackEnd.sqlite_db_connection import engine


async def create_all_tables() -> None:
    """
    Asynchronously create all tables in the database as defined in the ORM models.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All tables created successfully.")


if __name__ == "__main__":
    asyncio.run(create_all_tables())
