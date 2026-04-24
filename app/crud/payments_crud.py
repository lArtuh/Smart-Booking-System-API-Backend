from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sql.payment_models import Payment
from app.schemas.payments_schemas import PaymentCreate
from fastapi import HTTPException
from app.models.nosql.booking_model import Booking
# create payment


async def create_payment_crud(
    db: AsyncSession,
    booking: Booking,
    data: PaymentCreate,
    user_id: int
):
    new_payment = Payment(
        user_id=user_id,
        booking_id=str(booking.id),
        property_id=booking.property_id,
        amount=data.amount

    )

    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)

    await booking.set({"pay_id": new_payment.id})

    return new_payment

# get payment


async def get_payment_crud(
    db: AsyncSession,
    payment_id: int,
    user_id: int
):
    result = await db.execute(
        select(Payment).where(
            (Payment.id == payment_id) & (Payment.user_id == user_id)
        )
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment

# show all payments


async def show_all_payments_crud(db: AsyncSession, user_id: int):
    payments = await db.execute(select(Payment).where(Payment.user_id == user_id))
    result = payments.scalars().all()
    return result
