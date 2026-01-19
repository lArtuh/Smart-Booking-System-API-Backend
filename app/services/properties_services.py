from app.schemas.properties_schemas import PropertyCreate, PropertyUpdate
from fastapi import HTTPException
from app.models.nosql.property_model import Property
from app.crud.properties_crud import (
    create_property,
    get_property,
    show_all_properties,
    update_property,
    delete_property,
)
# create property


async def create_property_services(
    data: PropertyCreate,
    user_id: int
):

    new_property = create_property(user_id, data)
    return new_property


# get property


async def get_property_services(
    property_id: int,
    user_id: int
):

    property = get_property(property_id, user_id)
    return property


# show all properties

async def show_all_properties_services(user_id: str):
    properties = show_all_properties(user_id)
    return properties


# update property

async def update_property_service(property_id, user_id: str, data: PropertyUpdate):
    property = get_property(property_id, user_id)
    properties = update_property(property, data)
    return properties

# delete property


async def delete_property_services(user_id: str, property_id: str):

    property = get_property(property_id, user_id)
    property_deleted = delete_property(property)
    return property_deleted


# cancel property


async def cancel_property(property_id: str, user_id: str):
    property = await Property.find_one(
        (Property.id == property_id) & (Property.user_id == user_id)
    )
    if not property:
        raise HTTPException(status_code=404, detail="not found")
    await property.set({"status": "canceled"})
    return {"message": "canceled"}
