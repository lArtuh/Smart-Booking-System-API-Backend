from app.core.database import get_db
from fastapi import APIRouter, Depends
from app.models.sql.user_models import User
from app.schemas.payments_schemas import PaymentCreate, PaymentResponse
from app.auth.dependencies import get_current_user
from app.crud.payments_crud import (
    create_payment,
    show_payment,
    show_all_payments,
)

payment_router = APIRouter(prefix="/payments", tags=["payments"])


# create payment
@payment_router.post("/booking/{booking_id}", response_model=PaymentResponse)
async def create_payment_router(
    booking_id: int,
    data: PaymentCreate,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    new_payment = await create_payment(db, booking_id, data, current_user.id)
    return new_payment


# show payment
@payment_router.get("/{payment_id}", response_model=PaymentResponse)
async def show_payment_router(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    new_payment = await show_payment(db, current_user.id, payment_id)
    return new_payment


# show all payments
@payment_router.get("/", response_model=list[PaymentResponse])
async def show_all_payments_router(
    current_user: User = Depends(get_current_user),
    db=Depends(get_db)
):
    new_payment = await show_all_payments(db, current_user.id)
    return new_payment
