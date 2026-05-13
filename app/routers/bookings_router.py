from fastapi import APIRouter, Depends
from app.schemas.booking_schemas import BookingCreate, BookingUpdate, BookingResponse
from app.models.sql.user_models import User
from app.auth.dependencies import get_current_user
from app.services.booking_services import (
    create_booking_service,
    get_booking_service,
    show_all_user_bookings_services,
    update_booking_service,
    cancel_booking_service,
    delete_all_bookings_service
)

booking_router = APIRouter(prefix="/bookings", tags=["bookings"])

# create booking


@booking_router.post("/{property_id}", response_model=BookingResponse)
async def create_booking_router(
    property_id: str,
    data: BookingCreate,
    current_user: User = Depends(get_current_user)
):
    new_booking = await create_booking_service(property_id, data, current_user.id)
    return new_booking


# show booking

@booking_router.get("/{booking_id}", response_model=BookingResponse)
async def show_booking_router(
    booking_id: str,
    current_user: User = Depends(get_current_user)
):
    bookings = await get_booking_service(booking_id, current_user.id)
    return bookings

# show all user bookings


@booking_router.get("/", response_model=list[BookingResponse])
async def show_all_bookings_router(
    current_user: User = Depends(get_current_user)
):
    bookings = await show_all_user_bookings_services(current_user.id)
    return bookings

# update booking


@booking_router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking_router(
    booking_id: str,
    data: BookingUpdate,
    current_user: User = Depends(get_current_user)
):
    new_booking = await update_booking_service(booking_id, current_user.id, data)
    return new_booking


# cancel booking


@booking_router.patch("/cancel/{booking_id}", response_model=BookingResponse)
async def cancel_booking_router(
    booking_id: str,
    current_user: User = Depends(get_current_user)
):
    canceled_booking = await cancel_booking_service(booking_id, current_user.id)
    return canceled_booking


# delete all bookings
@booking_router.delete("/")
async def delete_all_properties_router():
    return await delete_all_bookings_services()
