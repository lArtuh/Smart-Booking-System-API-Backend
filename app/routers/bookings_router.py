from fastapi import APIRouter, Depends
from app.schemas.booking_schemas import BookingCreate, BookingUpdate, BookingResponse
from app.models.sql.user_models import User
from app.auth.dependencies import get_current_user
from app.crud.booking_crud import (
    create_booking,
    show_booking,
    show_all_bookings,
    update_booking,
    delete_booking,
    cancel_booking
)

booking_router = APIRouter(prefix="/bookings", tags=["bookings"])

# create booking


@booking_router.post("/", response_model=BookingResponse)
async def create_booking_router(
    data: BookingCreate,
    current_user: User = Depends(get_current_user)
):
    new_booking = await create_booking(data, current_user)
    return new_booking


# show booking

@booking_router.get("/{booking_id}", response_model=BookingResponse)
async def show_booking_router(
    booking_id: str,
    current_user: User = Depends(get_current_user)
):
    bookings = await show_booking(booking_id, current_user.id)
    return bookings

# show all bookings


@booking_router.get("/", response_model=list[BookingResponse])
async def show_all_bookings_router(
    current_user: User = Depends(get_current_user)
):
    bookings = await show_all_bookings(current_user.id)
    return bookings

# update booking


@booking_router.put("/{booking_id}")
async def update_booking_router(
    booking_id: str,
    data: BookingUpdate,
    current_user: User = Depends(get_current_user)
):
    new_booking = await update_booking(booking_id, current_user.id, data)
    return new_booking

# delete booking


@booking_router.delete("/{booking_id}")
async def delete_booking_router(
    booking_id: str,
    current_user: User = Depends(get_current_user)
):
    deleted_booking = await delete_booking(booking_id, current_user.id)
    return deleted_booking

# cancel booking


@booking_router.post("/{booking_id}/cancel")
async def cancel_booking_router(
    booking_id: str,
    current_user: User = Depends(get_current_user)
):
    canceled_booking = await cancel_booking(booking_id, current_user.id)
    return canceled_booking
