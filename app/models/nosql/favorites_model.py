from beanie import Document
from typing import List
from pydantic import Field


class Favorites(Document):
    user_id: int
    property_ids: List[str] = Field(default_factory=list)

    class Settings:
        name = "favorites"
