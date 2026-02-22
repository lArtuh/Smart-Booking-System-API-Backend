from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models.nosql.booking_model import Booking
from app.models.sql.payment_models import Payment
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
    payment_id = booking.pay_id
    if not payment_id:
        raise HTTPException(status_code=400, detail="Booking has no payment")

    payment: Payment = await get_payment(
        db,
        payment_id,
        user_id,
    )
    # user
    payment_user = payment.user_id == user_id
    if not payment_user:
        raise HTTPException(
            status_code=403, detail="Payment does not belong to this user")

    # property

    payment_property = payment.property_id == property_id

    if not payment_property:
        raise HTTPException(
            status_code=403, detail="Payment does not belong to this property")

    # paid

    payment_status = booking.status == "paid"

    if not payment_status:
        raise HTTPException(status_code=403, detail="Payment not complete")

    return payment
