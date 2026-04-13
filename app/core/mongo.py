from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.nosql.booking_model import Booking
from app.models.nosql.property_model import Property
from app.models.nosql.review_model import Review
from app.core.config import settings


DB_NAME = "smart_booking_db"


async def init_mongo():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[DB_NAME],
        document_models=[Booking, Property, Review]
    )
