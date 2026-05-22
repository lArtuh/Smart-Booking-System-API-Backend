from beanie import Document
from app.schemas.properties_schemas import PropertyCreate, PropertyUpdate, PropertyResponse
from app.models.nosql.property_model import Property
from fastapi import HTTPException
from app.crud.properties_crud import (
    create_property_crud,
    get_property_crud,
    show_all_user_properties_crud,
    show_all_properties_crud,
    update_property_crud,
    delete_property_crud,
    delete_all_properties_crud
)
# create property


async def create_property_services(user_id: int, data: PropertyCreate):

    prop = await create_property_crud(user_id, data)

    return await serialize(prop)

# show all user properties


async def show_all_user_properties_services(user_id: int):

    properties = await show_all_user_properties_crud(user_id)

    return [
        await serialize(p)
        for p in properties
    ]

# show all properties


async def show_all_properties_services():

    properties = await show_all_properties_crud()

    return [
        await serialize(p)
        for p in properties
    ]


# update property


async def update_property_service(
    property_id: str,
    user_id: int,
    data: PropertyUpdate
):

    prop = await get_property_crud(property_id)
    if prop.user_id != user_id:
        raise HTTPException(
            status_code=401, detail="Unauthorized")

    updated_property = await update_property_crud(property, data)

    return await serialize(updated_property)


# delete property


async def delete_property_services(property_id: str, user_id: int):
    prop = await get_property_crud(property_id)
    if prop.user_id != user_id:
        raise HTTPException(
            status_code=401, detail="Unauthorized")
    is_available = prop.status == "available" or "paused"
    if not is_available:
        raise HTTPException(
            status_code=403, detail="property has active bookings")
    await delete_property_crud(prop)
    return {"menssage": "Property deleted successfully"}

# delete all properties


async def delete_all_properties_services():
    await delete_all_properties_crud()
    return {"menssage": "All properties deleted successfully"}

# delete all user properties


async def delete_all_user_properties_services(user_id: int):
    prop: list[Property] = await show_all_user_properties_crud(user_id)
    for p in prop:
        await delete_property_crud(p)
    return {"menssage": "All properties deleted successfully"}


# pause property


async def pause_property(property_id: str, user_id: int):
    prop = await get_property_crud(property_id)
    if prop.user_id != user_id:
        raise HTTPException(
            status_code=401, detail="Unauthorized")
    is_reserved = prop.status == "reserved"
    if is_reserved:
        raise HTTPException(
            status_code=403, detail="property has active bookings")
    is_paused = prop.status == "paused"
    if is_paused:
        raise HTTPException(
            status_code=409, detail="this property is already paused")
    await prop.set({"status": "paused"})

    return PropertyResponse(
        id=str(prop.id),
        user_id=prop.user_id,
        status=prop.status
    )


async def serialize(object: Document):
    data = object.model_dump()
    data["id"] = str(object.id)
    return data
