from app.core.database import get_db
from fastapi import APIRouter, Depends
from app.models.sql.user_models import User
from app.schemas.payments_schemas import PaymentCreate, PaymentResponse
from app.auth.dependencies import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.payment_services import (
    make_payment_service,
    get_payment_service,
    show_all_payments_service,
)

payment_router = APIRouter(prefix="/payments", tags=["payments"])


# create payment
@payment_router.post("/{booking_id}", response_model=PaymentResponse)
async def create_payment_router(
    booking_id: str,
    data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    new_payment = await make_payment_service(db, booking_id, data, current_user.id)
    return new_payment


# show payment
@payment_router.get("/{payment_id}", response_model=PaymentResponse)
async def show_payment_router(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_payment = await get_payment_service(db, payment_id, current_user.id)
    return new_payment


# show all payments
@payment_router.get("/", response_model=list[PaymentResponse])
async def show_all_payments_router(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    new_payment = await show_all_payments_service(db, current_user.id)
    return new_payment
