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
    customer_id: int
    owner_id: int
    property_id: str
    pay_status: str
    pay_id: int | None
    canceled: bool
    paused: bool
