from pydantic import BaseModel, Field
from datetime import datetime


class ReviewBase(BaseModel):
    points: int = Field(ge=1, le=5)
    description: str


class ReviewCreate(ReviewBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReviewResponse(ReviewBase):
    id: str
    user_id: int
    created_at: datetime
    property_id: str
