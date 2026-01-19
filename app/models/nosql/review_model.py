from beanie import Document
from datetime import datetime
from pydantic import Field


class Review(Document):
    user_id: str
    property_id: str
    points: int
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "Review"
