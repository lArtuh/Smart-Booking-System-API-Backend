from fastapi import APIRouter, Depends
from app.schemas.favorites_schemas import FavoritesResponse
from app.models.sql.user_models import User
from app.auth.dependencies import get_current_user
from app.services.favorites_services import (
    create_favorite_services,
    show_all_favorites_services,
    delete_favorite_services,
    delete_all_favorites_services
)

favorite_router = APIRouter(prefix="/favorites", tags=["favorites"])


# create favorite
@favorite_router.post("/{property_id}", response_model=FavoritesResponse)
async def create_favorite_router(
    property_id: str,
    current_user: User = Depends(get_current_user)
):
    return await create_favorite_services(current_user.id, property_id)


# show all user favorites
@favorite_router.get("/", response_model=FavoritesResponse)
async def show_all_user_favorites_router(
    current_user: User = Depends(get_current_user)
):
    return await show_all_favorites_services(current_user.id)


# delete favorite


@favorite_router.delete("/{property_id}")
async def delete_favorite_router(
    property_id: str,
    current_user: User = Depends(get_current_user)
):
    return await delete_favorite_services(current_user.id, property_id)


# delete all favorites


@favorite_router.delete("/")
async def delete_all_favorites_router():
    return await delete_all_favorites_services()
