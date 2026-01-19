from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.nosql.booking_model import Booking
from app.models.nosql.property_model import Property

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "my_database"


async def init_mongo():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(
        database=client[DB_NAME],
        document_models=[Booking, Property]
    )
