from beanie import Document
from datetime import datetime
from typing import List
from pydantic import Field, ConfigDict
from bson import ObjectId


class Property(Document):
    user_id: int
    title: str
    description: str
    address: str
    city: str
    country: str
    price_per_night: float = 0
    status: str = "available"
    favorites_count: int = 0
    amenities: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "properties"
