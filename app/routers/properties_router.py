from fastapi import APIRouter, Depends
from app.schemas.properties_schemas import PropertyResponse, PropertyCreate, PropertyUpdate
from app.models.sql.user_models import User
from app.auth.dependencies import get_current_user
from app.crud.properties_crud import (
    create_property,
    show_property,
    show_all_properties,
    update_property,
    delete_property,
    cancel_property
)

property_router = APIRouter(prefix="/properties", tags=["properties"])


# create property
@property_router.post("/", response_model=PropertyResponse)
async def create_property_router(
    data: PropertyCreate,
    current_user: User = Depends(get_current_user)
):
    return await create_property(current_user.id, data)


# show property
@property_router.get("/{property_id}", response_model=PropertyResponse)
async def show_property_router(
    property_id: str,
    current_user: User = Depends(get_current_user)
):
    return await show_property(property_id, current_user.id)


# show all properties
@property_router.get("/", response_model=list[PropertyResponse])
async def show_all_properties_router(
    current_user: User = Depends(get_current_user)
):
    return await show_all_properties(current_user.id)


# update property
@property_router.put("/{property_id}")
async def update_property_router(
    property_id: str,
    data: PropertyUpdate,
        current_user: User = Depends(get_current_user)
):
    return await update_property(property_id, current_user.id, data)

# delete property


@property_router.delete("/{property_id}")
async def delete_property_router(
    property_id: str,
    current_user: User = Depends(get_current_user)
):
    return await delete_property(property_id, current_user.id)


# cancel property
@property_router.post("/{property_id}/cancel")
async def cancel_property_router(
    property_id: str,
    current_user: User = Depends(get_current_user)
):
    return await cancel_property(property_id, current_user.id)
