from app.models.nosql.property_model import Property
from app.schemas.properties_schemas import PropertyCreate, PropertyUpdate
from fastapi import HTTPException


# create property
async def create_property(user_id: str, data: PropertyCreate):
    new_property = Property(**data.model_dump())
    new_property.user_id = user_id
    await new_property.insert()
    return new_property


# show property

async def show_property(property_id: str, user_id: str):
    property = await Property.find_one(
        (Property.id == property_id) & (Property.user_id == user_id)
    )
    if not property:
        raise HTTPException(status_code=404, detail="not found")
    return property


# show all properties

async def show_all_properties(user_id: str):
    properties = await Property.find(Property.user_id == user_id).to_list()
    return properties


# update property
async def update_property(property_id: str, user_id: str, data: PropertyUpdate):
    property = await Property.find_one(
        (Property.id == property_id) & (Property.user_id == user_id)
    )
    if not property:
        raise HTTPException(status_code=404, detail="not found")
    await property.set(data.model_dump(exclude_unset=True))
    return {"message": "Property updated successfully"}

# delete property


async def delete_property(user_id: str, property_id: str):
    property = await Property.find_one(
        (Property.id == property_id) & (Property.user_id == user_id)
    )
    if not property:
        raise HTTPException(status_code=404, detail="not found")
    await property.delete()
    return {"mensage": "Property deleted successfully"}

# cancel property


async def cancel_property(property_id: str, user_id: str):
    property = await Property.find_one(
        (Property.id == property_id) & (Property.user_id == user_id)
    )
    if not property:
        raise HTTPException(status_code=404, detail="not found")
    await property.set({"status": "canceled"})
    return {"message": "canceled"}
