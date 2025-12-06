from app.models.nosql.booking_models import Booking
from app.models.nosql.property_model import Property
from app.schemas.booking_schemas import BookingCreate, BookingUpdate
from fastapi import HTTPException
# create booking


async def create_booking(data: BookingCreate, user_id: str):
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
    await new_booking.insert()
    prop.status = "reserved"
    await prop.save()
    return new_booking


# show booking


async def show_booking(booking_id: str, user_id: str):
    booking = await Booking.find_one(
        (Booking.id == booking_id) & (Booking.user_id == user_id)
    )
    if not booking:
        raise HTTPException(status_code=404, detail="not found")
    return booking


# show all bookings

async def show_all_bookings(user_id: str):
    bookings = await Booking.find(Booking.user_id == user_id).sort("start_date").to_list()
    return bookings


# update booking
async def update_booking(booking_id: str, user_id: str, data: BookingUpdate):
    booking = await Booking.find_one(
        (Booking.id == booking_id) & (Booking.user_id == user_id)
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    await booking.set(data.model_dump(exclude_unset=True))
    return {"message": "Booking updated successfully"}

# delete booking


async def delete_booking(user_id: str, booking_id: str):
    booking = await Booking.find_one(
        (Booking.id == booking_id) & (Booking.user_id == user_id)
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    await booking.delete()
    prop = await Property.get(booking.property_id)
    if not prop:
        raise HTTPException(status_code=404,
                            detail="This booking does not belong to the property")
    prop.status = "available"
    return {"message": "Booking deleted successfully"}

# cancel booking


async def cancel_booking(booking_id: str, user_id: str):
    booking = await Booking.find_one(
        (Booking.id == booking_id) & (Booking.user_id == user_id)
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    await booking.set({"status": "canceled"})
    return {"message": "Booking canceled successfully"}
