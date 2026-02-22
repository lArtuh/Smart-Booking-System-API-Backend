import asyncio
from sqlalchemy import text
from app.core.database import async_session


async def test_db():
    async with async_session() as session:
        result = await session.execute(text("SELECT 1"))
        print("DB OK:", result.scalar())

if __name__ == "__main__":
    asyncio.run(test_db())
