from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    second_name = Column(String(50))
    email = Column(String(120), unique=True, index=True)
    hashed_password = Column(String(200), nullable=False)
    create_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
