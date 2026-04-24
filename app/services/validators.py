from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models.nosql.booking_model import Booking
from app.crud.payments_crud import get_payment

# validate booking


def validate_booking_for_review(booking: Booking):
    if booking.status == "canceled":
        raise HTTPException(status_code=400, detail="Booking was canceled")

    if datetime.utcnow() < booking.end_date:
        raise HTTPException(
            status_code=400,
            detail="Booking not finished yet"
        )


# validate payment


async def validate_payment(
    booking: Booking,
    db: AsyncSession,
    user_id: int,
    property_id: str
):

    if not booking.pay_id or booking.status != "paid":
        raise HTTPException(status_code=403, detail="Payment not complete")

    payment = await get_payment(
        db,
        booking.pay_id,
        user_id,
    )
    # validate user and property
    if payment.user_id != user_id or payment.property_id != property_id:
        raise HTTPException(
            status_code=401, detail="unauthorized"
        )

    return payment
