from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from app.models.nosql.booking_model import Booking
from app.models.sql.payment_models import Payment
from app.schemas.payments_schemas import PaymentCreate
from app.models.sql.payment_models import Payment
from app.crud.payments_crud import (
    create_payment,
    get_payment,
    show_all_payments,
)


# pay
async def make_payment_service(
    db: AsyncSession,
    booking_id: int,
    data: PaymentCreate,
    user_id: int
):

    booking = await Booking.find_one(Booking.id == booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(
        select(Payment).where(Payment.booking_id == booking_id)
    )
    existing_payment = result.scalar_one_or_none()
    if existing_payment:
        raise HTTPException(status_code=400, detail="Booking already paid")

    booking.status = "paid"
    await booking.save()

    new_payment = create_payment(db, booking_id, data, user_id)
    return new_payment

# get payment


async def get_payment_service(
    db: AsyncSession,
    payment_id: str,
    user_id: str
):
    pay = get_payment(db, user_id, payment_id)
    return pay


# show all user payments
async def show_all_payments_service(
        db: AsyncSession, user_id: int
):
    payments = show_all_payments(db, user_id)
    return payments
