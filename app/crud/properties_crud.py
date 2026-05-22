from app.models.nosql.property_model import Property
from app.schemas.properties_schemas import PropertyCreate, PropertyUpdate
from fastapi import HTTPException
from beanie import PydanticObjectId

# create property


async def create_property_crud(user_id: int, data: PropertyCreate):
    new_property = Property(
        **data.model_dump(),
        user_id=user_id
    )
    await new_property.insert()
    return new_property


# show property

async def get_property_crud(property_id: str):
    try:
        property_oid = PydanticObjectId(property_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    prop = await Property.find_one(
        Property.id == property_oid,
    )
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop


# show all user properties

async def show_all_user_properties_crud(user_id: int):
    properties = await Property.find(Property.user_id == user_id).to_list()
    return properties


# show user properties

async def show_all_properties_crud():
    properties = await Property.find(
        Property.status != "paused").to_list()
    return properties


# update property
async def update_property_crud(property: Property, data: PropertyUpdate):

    await property.update({
        "$set": data.model_dump(exclude_unset=True)
    })

    return property

# delete property


async def delete_property_crud(prop: Property):
    await prop.delete()


# delete all properties

async def delete_all_properties_crud():
    await Property.find_all().delete()
