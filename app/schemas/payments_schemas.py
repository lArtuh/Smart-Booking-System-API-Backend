from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class PaymentBase(BaseModel):
    user_id: int
    booking_id: str
    amount: Decimal


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    date: datetime | None = None
    amount: Decimal | None = None


class PaymentResponse(PaymentBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True
