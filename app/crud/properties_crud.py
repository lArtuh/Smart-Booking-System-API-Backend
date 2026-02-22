from app.models.nosql.property_model import Property
from app.schemas.properties_schemas import PropertyCreate, PropertyUpdate
from fastapi import HTTPException
from beanie import PydanticObjectId

# create property


async def create_property(user_id: str, data: PropertyCreate):
    new_property = Property(
        **data.model_dump(),
        user_id=user_id
    )

    await new_property.insert()
    return new_property


# show property

async def get_property(property_id: str, user_id: str):
    try:
        object_id = PydanticObjectId(property_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    property = await Property.find_one(
        Property.id == object_id,
        Property.user_id == user_id
    )
    if not property:
        raise HTTPException(status_code=404, detail="not found")
    return property


# show all user properties

async def show_all_user_properties_crud(user_id: str):
    properties = await Property.find(Property.user_id == user_id).to_list()
    return properties


# show user properties

async def show_all_properties_crud():
    properties = await Property.find_all().to_list()
    return properties


# update property
async def update_property(property: Property, data: PropertyUpdate):

    await property.update({
        "$set": data.model_dump(exclude_unset=True)
    })

    return property

# delete property


async def delete_property(property: Property):
    await property.delete()
    return {"mensage": "Property deleted successfully"}
