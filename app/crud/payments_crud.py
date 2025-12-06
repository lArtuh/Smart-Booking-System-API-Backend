from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.nosql.booking_models import Booking
from app.models.sql.payment_models import Payment
from app.schemas.payments_schemas import PaymentCreate
from fastapi import HTTPException

# create payment


async def create_payment(
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

    new_payment = Payment(
        user_id=user_id,
        booking_id=booking_id,
        amount=data.amount
    )

    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)

    return new_payment


# show payment
async def show_payment(db: AsyncSession, user_id: int, payment_id: int):
    payment = await db.execute(
        select(Payment).where(
            (Payment.user_id == user_id) &
            (Payment.id == payment_id)
        )
    )
    result = payment.scalars().one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Payments not found")

    return result


# show all payments
async def show_all_payments(db: AsyncSession, user_id: int):
    payments = await db.execute(select(Payment).where(Payment.user_id == user_id))
    result = payments.scalars().all()
    return result
