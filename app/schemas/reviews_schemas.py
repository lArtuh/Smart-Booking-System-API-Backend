from pydantic import BaseModel, Field
from datetime import datetime


class ReviewBase(BaseModel):
    points: int = Field(ge=1, le=5)
    description: str


class ReviewCreate(ReviewBase):
    user_id: str
    property_id: str
    date: datetime = Field(default_factory=datetime.utcnow)


class ReviewUpdate(BaseModel):
    points: int | None = Field(default=None, ge=1, le=5)
    description: str | None = None
    date: datetime = Field(default_factory=datetime.utcnow)


class ReviewResponse(ReviewBase):
    id: str
    user_id: str
