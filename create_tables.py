import asyncio
from app.core.database import engine, Base

# IMPORTA TODOS LOS MODELOS
from app.models.sql.user_models import User
# cuando tengas más:
# from app.models.property import Property
# from app.models.booking import Booking


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.meta)

if __name__ == "__main__":
    asyncio.run(create_tables())


print(Base.metadata)
print(dir(Base.metadata))
