from pydantic import BaseModel
from beanie import PydanticObjectId


class PropertyBase(BaseModel):
    title: str
    description: str
    address: str
    city: str
    country: str
    price_per_night: float | None = None


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    price_per_night: float | None = None


class PropertyResponse(PropertyBase):
    id: str
    user_id: int
    status: str
