from pydantic import BaseModel
from datetime import datetime


class BookingBase(BaseModel):
    start_date: datetime
    end_date: datetime


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None


class BookingResponse(BookingBase):
    id: str
    user_id: int
    owner_id: int
    property_id: str
    status: str | None = "pending"
    pay_id: int | None = None
