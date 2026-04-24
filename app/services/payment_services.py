from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from app.models.nosql.booking_model import Booking
from app.models.sql.payment_models import Payment
from app.schemas.payments_schemas import PaymentCreate
from app.crud.booking_crud import get_booking_crud
from app.crud.payments_crud import (
    create_payment_crud,
    get_payment_crud,
    show_all_payments_crud,
)


# pay
async def make_payment_service(
    db: AsyncSession,
    booking_id: Booking,
    data: PaymentCreate,
    user_id: int
):

    booking = await get_booking_crud(booking_id, user_id)

    if booking.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(
        select(Payment).where(Payment.booking_id == booking_id)
    )
    existing_payment = result.scalar_one_or_none()
    if existing_payment:
        raise HTTPException(status_code=400, detail="Booking already paid")

    new_payment = await create_payment_crud(db, booking, data, user_id)
    return new_payment

# get payment


async def get_payment_service(
    db: AsyncSession,
    payment_id: int,
    user_id: int
):
    pay = await get_payment_crud(db, payment_id, user_id)
    return pay


# show all user payments
async def show_all_payments_service(
        db: AsyncSession,
        user_id: int
):
    payments = await show_all_payments_crud(db, user_id)
    return payments
