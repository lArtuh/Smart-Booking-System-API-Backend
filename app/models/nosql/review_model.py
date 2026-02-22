from beanie import Document
from datetime import datetime
from pydantic import Field
from pydantic import ConfigDict
from bson import ObjectId


class Review(Document):
    user_id: int
    booking_id: str
    property_id: str
    points: int
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        json_encoders={
            ObjectId: str
        }
    )

    class Settings:
        name = "reviews"
