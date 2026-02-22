from beanie import Document, PydanticObjectId
from datetime import datetime
from typing import List
from pydantic import Field


class Property(Document):
    user_id: int
    title: str
    description: str
    address: str
    city: str
    country: str
    price_per_night: float = 0
    status: str = "available"
    amenities: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "properties"
