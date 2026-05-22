from app.models.nosql.booking_model import Booking
from app.schemas.booking_schemas import BookingUpdate
from app.services.properties_services import serialize
from app.crud.properties_crud import get_property_crud
from fastapi import HTTPException
from beanie import PydanticObjectId

# create booking


async def create_booking_crud(new_booking: Booking):
    await new_booking.insert()
    return new_booking


# show booking

async def get_booking_crud(
    booking_id: str,
    user_id: int,
):

    try:
        booking_oid = PydanticObjectId(booking_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    booking = await Booking.find_one(
        Booking.id == booking_oid,
        Booking.customer_id == user_id
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking

# show all user bookings


async def show_all_user_bookings_crud(user_id: int):
    bookings = await Booking.find(Booking.customer_id == user_id).sort("start_date").to_list()
    return bookings


# show all properties bookings


async def show_all_properties_bookings_crud(property_id: str):
    bookings = await Booking.find(Booking.property_id == int(property_id)).to_list()
    return bookings

# update booking


async def update_booking_crud(booking: Booking, data: BookingUpdate):
    await booking.set(data.model_dump(exclude_unset=True))
    return booking

# delete booking

# async def delete_booking(user_id: str, booking_id: str):
#     booking = await get_booking(booking_id,user_id)
#     prop = await get_property(booking.property_id,user_id)
#     await booking.delete()
#     prop.status = "available"
#     return {"message": "Booking deleted successfully"}


# delete all bookings

async def delete_all_bookings_crud():
    await Booking.find_all().delete()
