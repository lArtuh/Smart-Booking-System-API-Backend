from beanie import Document
from datetime import datetime


class Booking(Document):

    property_id: str
    user_id: int
    owner_id: int
    start_date: datetime
    end_date: datetime
    status: str = "pending"
    pay_id: int | None = None

    class Settings:
        name = "bookings"
