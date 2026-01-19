from sqlalchemy import Column, Integer, Numeric, String, DateTime
from app.core.database import Base
from datetime import datetime


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    property_id = Column(Integer, nullable=False)
    booking_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False, default="pending", index=True)
