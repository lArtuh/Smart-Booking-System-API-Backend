from beanie import Document
from datetime import datetime


class Booking(Document):
    user_id: str
    owner_id: str
    property_id: str
    start_date: datetime
    end_date: datetime
    status: str = "pending"
    pay_id: int = None

    class Settings:
        name = "bookings"
