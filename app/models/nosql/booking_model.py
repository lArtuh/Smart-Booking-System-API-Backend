from beanie import Document
from datetime import datetime


class Booking(Document):

    property_id: str
    customer_id: int
    owner_id: int
    start_date: datetime
    end_date: datetime
    pay_status: str = "pending"
    pay_id: int | None = None
    canceled: bool = False
    paused: bool = False

    class Settings:
        name = "bookings"
