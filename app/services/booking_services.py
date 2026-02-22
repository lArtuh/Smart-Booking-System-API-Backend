from app.schemas.booking_schemas import BookingCreate, BookingUpdate, BookingResponse
from app.models.nosql.booking_model import Booking
from app.models.nosql.property_model import Property
from fastapi import HTTPException
from app.crud.booking_crud import get_booking
from beanie import PydanticObjectId
from app.crud.booking_crud import (
    create_booking,
    get_booking,
    show_all_bookings,
    update_booking
)

# create booking


async def create_booking_service(
    property_id: str,
    data: BookingCreate,
    user_id: int
):
    try:
        property_oid = PydanticObjectId(property_id)
    except:
        raise HTTPException(400, "Invalid property id")
    prop = await Property.get(property_oid)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    if prop.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="You cannot book your own prop")
    if prop.status == "paused":
        raise HTTPException(status_code=404, detail="Property not available")

    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be earlier than start date"
        )
    overlap = await Booking.find_one(
        Booking.property_id == property_id,
        Booking.end_date >= data.start_date,
        Booking.start_date <= data.end_date
    )
    if overlap:
        raise HTTPException(
            status_code=400,
            detail="This property is already booked for this date range"
        )
    new_booking = Booking(
        **data.model_dump(),
        property_id=property_id,
        user_id=user_id,
        owner_id=prop.user_id
    )

    booking = await create_booking(new_booking)

    prop.status = "reserved"
    await prop.save()

    data = booking.model_dump()
    data["id"] = str(booking.id)

    return BookingResponse(**data)

# show booking


async def get_booking_service(
    booking_id: str,
    user_id: int,
):
    booking = await get_booking(booking_id, user_id)

    data = booking.model_dump()

    data["id"] = str(booking.id)

    return BookingResponse(**data)

# show all bookings


async def show_all_bookings_services(user_id: int):
    bookings = await show_all_bookings(user_id)

    return [
        BookingResponse(
            **{
                **b.model_dump(),
                "id": str(b.id),
            }
        )
        for b in bookings
    ]
# update booking


async def update_booking_service(
    booking_id: str,
    user_id: int,
    data: BookingUpdate
):
    booking = await get_booking(booking_id, user_id)

    booking = await update_booking(booking, data)

    data_booking = booking.model_dump()
    data_booking["id"] = str(booking.id)

    return BookingResponse(**data_booking)

# cancel booking


async def cancel_booking(booking_id: str, user_id: int):
    booking: Booking = await get_booking(booking_id, user_id)
    if booking.status == "canceled":
        raise HTTPException(400, "Booking already canceled")
    await booking.set({"status": "canceled"})

    data_booking = booking.model_dump()
    data_booking["id"] = str(booking.id)

    return BookingResponse(**data_booking)
