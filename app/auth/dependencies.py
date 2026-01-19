from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.jwt_handler import oauth2_scheme, verify_token
from app.core.database import get_db
from app.models.sql.user_models import User
from app.models.nosql.booking_model import Booking


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = verify_token(token)
    user_id: str = payload.get("sub")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def get_current_property(
    booking_id: str,
    user_id=Depends(get_current_user)
):
    booking = await Booking.find_one(
        Booking.user_id == user_id,
        Booking.id == booking_id
    )
    if not booking:
        raise HTTPException(status_code=404, detail="booking not found")

    return booking.property_id
