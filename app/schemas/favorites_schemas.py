from pydantic import BaseModel, Field
from typing import List


class FavoritesBase(BaseModel):
    pass


class FavoritesCreate(FavoritesBase):
    property_id: str


# class FavoritesUpdate(BaseModel):
#     property_ids: List[str] = Field(default_factory=list)


class FavoritesResponse(FavoritesBase):
    property_ids: List[str] = Field(default_factory=list)
