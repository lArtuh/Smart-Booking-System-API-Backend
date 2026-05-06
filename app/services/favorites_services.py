from app.schemas.favorites_schemas import FavoritesCreate
from app.services.properties_services import serialize
from fastapi import HTTPException
from app.crud.favorites_crud import (
    create_favorites_crud,
    update_favorites_crud,
    get_all_favorites_crud,
    get_one_favorite_crud,
    delete_favorite_crud
)

# create favorite


async def create_favorite_services(user_id: int, property_id: str):
    favorites = await get_all_favorites_crud(user_id)
    if not favorites:
        new_favorites = await create_favorites_crud(user_id, property_id)
    else:
        new_favorites = await update_favorites_crud(favorites, property_id)
    return await serialize(new_favorites)

# show all user favorites


async def show_all_favorites_services(user_id: int):

    favorites = await get_all_favorites_crud(user_id)
    if not favorites:
        return {"property_ids": []}
    return await serialize(favorites)


# delete favorite
async def delete_favorite_services(user_id: int, property_id: str):
    favorite = await get_one_favorite_crud(user_id, property_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="not found")
    await delete_favorite_crud(favorite, property_id)
    favorites = await get_all_favorites_crud(user_id)
    return await serialize(favorites)
