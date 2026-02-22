from app.core.database import engine, Base
import app.models  # 👈 IMPORTANTÍSIMO


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
