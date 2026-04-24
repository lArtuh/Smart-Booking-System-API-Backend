from app.schemas.booking_schemas import BookingCreate, BookingUpdate
from app.models.nosql.booking_model import Booking
from app.services.properties_services import serialize
from fastapi import HTTPException
from beanie import PydanticObjectId
from app.crud.properties_crud import get_property
from app.crud.booking_crud import (
    create_booking_crud,
    get_booking_crud,
    show_all_bookings_crud,
    update_booking_crud
)

# create booking


async def create_booking_service(
    property_id: str,
    data: BookingCreate,
    user_id: int
):
    prop = await get_property(property_id, str(user_id))
    if prop.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="You can not book your own prop")
    if prop.status == "paused":
        raise HTTPException(status_code=404, detail="Property not available")

    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be earlier than start date"
        )
    overlap = await Booking.find_one(
        Booking.status != "paused",
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

    booking = await create_booking_crud(new_booking)

    prop.status = "reserved"
    await prop.save()

    # data = booking.model_dump()
    # data["id"] = str(booking.id)
    # return BookingResponse(**data)
    return await serialize(booking)

# show booking


async def get_booking_service(
    booking_id: str,
    user_id: int,
):
    booking = await get_booking_crud(booking_id, user_id)

    # data = booking.model_dump()
    # data["id"] = str(booking.id)
    # return BookingResponse(**data)
    return await serialize(booking)

# show all user bookings


async def show_all_user_bookings_services(user_id: int):
    bookings = await show_all_bookings_crud(user_id)

    # return [
    #     BookingResponse(
    #         **{
    #             **b.model_dump(),
    #             "id": str(b.id),
    #         }
    #     )
    #     for b in bookings
    # ]

    return [
        await serialize(b)
        for b in bookings
    ]


# update booking


async def update_booking_service(
    booking_id: str,
    user_id: int,
    data: BookingUpdate
):
    booking = await get_booking_crud(booking_id, user_id)

    booking = await update_booking_crud(booking, data)

    # data = booking.model_dump()
    # data["id"] = str(booking.id)
    # return BookingResponse(**data)
    return await serialize(booking)

# cancel booking


async def cancel_booking_service(booking_id: str, user_id: int):
    booking: Booking = await get_booking_crud(booking_id, user_id)
    if booking.status == "canceled":
        raise HTTPException(400, "Booking already canceled")
    await booking.set({"status": "canceled"})

    # data = booking.model_dump()
    # data["id"] = str(booking.id)
    # return BookingResponse(**data)
    return await serialize(booking)
