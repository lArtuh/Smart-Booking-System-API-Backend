from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sql.payment_models import Payment
from app.schemas.payments_schemas import PaymentCreate
from fastapi import HTTPException
from app.crud.booking_crud import get_booking
from app.models.nosql.booking_model import Booking
# create payment


async def create_payment(
    db: AsyncSession,
    booking_id: int,
    data: PaymentCreate,
    user_id: int
):
    new_payment = Payment(
        user_id=user_id,
        booking_id=booking_id,
        amount=data.amount
    )
    booking: Booking = get_booking(booking_id, user_id)
    await booking.set(
        {"status": "paid"},
        {"pay_id": new_payment.id}
    )

    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)

    return new_payment

# get payment


async def get_payment(
    db: AsyncSession,
    user_id: str,
    payment_id: str
):
    result = await db.execute(
        select(Payment).where(
            Payment.id == payment_id & Payment.user_id == user_id
        )
    )
    payment = result.scalars().first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment

# show all payments


async def show_all_payments(db: AsyncSession, user_id: int):
    payments = await db.execute(select(Payment).where(Payment.user_id == user_id))
    result = payments.scalars().all()
    return result
