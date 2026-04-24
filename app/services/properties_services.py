from beanie import Document
from pydantic import BaseModel
from app.schemas.properties_schemas import PropertyCreate, PropertyUpdate, PropertyResponse
from fastapi import HTTPException
from app.models.nosql.property_model import Property
from app.crud.properties_crud import (
    create_property_crud,
    get_property_crud,
    show_all_user_properties_crud,
    show_all_properties_crud,
    update_property_crud,
    delete_property_crud,
)
# create property


async def create_property_services(user_id: int, data: PropertyCreate):

    property = await create_property_crud(user_id, data)

    return await serialize(property)

# show all user properties


async def show_all_user_properties_services(user_id: str):

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
    user_id: str,
    data: PropertyUpdate
):

    property = await get_property_crud(property_id, user_id)

    updated_property = await update_property_crud(property, data)

    return await serialize(updated_property)


# delete property


async def delete_property_services(property_id: str, user_id: str):
    property: Property = await get_property_crud(property_id, user_id)
    is_available = property.status == "available" or "paused"
    if not is_available:
        raise HTTPException(
            status_code=403, detail="property has active bookings")
    await delete_property_crud(property)
    return {"menssage": "Property deleted successfully"}


# pause property


async def pause_property(property_id: str, user_id: str):
    property: Property = await get_property_crud(property_id, user_id)
    is_reserved = property.status == "reserved"
    if is_reserved:
        raise HTTPException(
            status_code=403, detail="property has active bookings")
    is_paused = property.status == "paused"
    if is_paused:
        raise HTTPException(
            status_code=409, detail="this property is already paused")
    await property.set({"status": "paused"})

    return PropertyResponse(
        id=str(property.id),
        user_id=property.user_id,
        status=property.status
    )


# Mapear un modelo a un response, ajustando el id


async def serialize(object: Document):
    BaseModel(
        **object.model_dump(), id=str(object.id)
    )

# async def serialize(property: Property):
#     PropertyResponse(
#         **property.model_dump(), id=str(property.id)
#     )
