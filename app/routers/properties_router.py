from fastapi import APIRouter, Depends
from app.schemas.properties_schemas import PropertyResponse, PropertyCreate, PropertyUpdate
from app.models.sql.user_models import User
from app.auth.dependencies import get_current_user
from app.services.properties_services import (
    create_property_services,
    get_property_services,
    show_all_properties_services,
    update_property_service,
    delete_property_services,
)

property_router = APIRouter(prefix="/properties", tags=["properties"])


# create property
@property_router.post("/", response_model=PropertyResponse)
async def create_property_router(
    data: PropertyCreate,
    current_user: User = Depends(get_current_user)
):
    return await create_property_services(current_user.id, data)


# show property
@property_router.get("/{property_id}", response_model=PropertyResponse)
async def show_property_router(
    property_id: str,
    current_user: User = Depends(get_current_user)
):
    return await get_property_services(property_id, current_user.id)


# show all properties
@property_router.get("/", response_model=list[PropertyResponse])
async def show_all_properties_router(
    current_user: User = Depends(get_current_user)
):
    return await show_all_properties_services(current_user.id)


# update property
@property_router.put("/{property_id}")
async def update_property_router(
    property_id: str,
    data: PropertyUpdate,
        current_user: User = Depends(get_current_user)
):
    return await update_property_service(property_id, current_user.id, data)

# delete property


@property_router.delete("/{property_id}")
async def delete_property_router(
    property_id: str,
    current_user: User = Depends(get_current_user)
):
    return await delete_property_services(property_id, current_user.id)
