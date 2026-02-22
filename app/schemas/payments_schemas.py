from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class PaymentBase(BaseModel):
    amount: Decimal


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int
    date: datetime
    booking_id: str
    property_id: str

    class Config:
        from_attributes = True
