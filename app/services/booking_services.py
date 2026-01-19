from app.schemas.booking_schemas import BookingCreate, BookingUpdate
from app.models.nosql.booking_model import Booking
from app.models.nosql.property_model import Property
from fastapi import HTTPException
from app.crud.booking_crud import get_booking
from app.crud.booking_crud import (
    create_booking,
    get_booking,
    show_all_bookings,
    update_booking
)

# create booking


async def create_booking_service(
    user_id: int,
    data: BookingCreate,
):
    prop = await Property.get(data.property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    if prop.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="You cannot book your own prop")
    if prop.status != "available":
        raise HTTPException(status_code=404, detail="Property not available")

    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be earlier than start date"
        )
    overlap = await Booking.find_one(
        (Booking.property_id == data.property_id) &
        (Booking.end_date >= data.start_date) &
        (Booking.start_date <= data.end_date)
    )
    if overlap:
        raise HTTPException(
            status_code=400,
            detail="This property is already booked for this date range"
        )
    new_booking = Booking(
        **data.model_dump(),
        user_id=user_id,
        owner_id=prop.user_id
    )

    review = await create_booking(new_booking)
    prop.status = "reserved"
    await prop.save()
    return review

# show booking


async def get_booking_service(
    booking_id: str,
    user_id: int,
):
    boking = get_booking(booking_id, user_id)
    return boking

# show all bookings


async def show_all_bookings_services(user_id: str):
    bokings = show_all_bookings(user_id)
    return bokings
# update booking


async def update_booking_service(booking_id: str, user_id: str, data: BookingUpdate):
    booking = get_booking(booking_id, user_id)
    updated_booking = update_booking(booking, data)
    return updated_booking
# cancel booking


async def cancel_booking(booking_id: str, user_id: int):
    booking: Booking = get_booking(booking_id, user_id)
    await booking.set({"status": "canceled"})
    return {"message": "Booking canceled successfully"}
