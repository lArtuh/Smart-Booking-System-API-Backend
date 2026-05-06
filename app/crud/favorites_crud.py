from app.models.nosql.favorites_model import Favorites
from app.crud.properties_crud import get_property_crud
from app.schemas.favorites_schemas import FavoritesCreate


# create favorites

async def create_favorites_crud(user_id: int, property_id: str):
    new_favorites = Favorites(
        user_id=user_id,
        property_ids=[property_id]
    )
    await new_favorites.insert()
    prop = await get_property_crud(property_id)
    await prop.update({"$inc": {"favorites_count": 1}})
    return new_favorites


# update favorites
async def update_favorites_crud(favorites: Favorites, property_id: str):
    await favorites.update({"$addToSet": {"property_ids": property_id}})
    prop = await get_property_crud(property_id)
    await prop.update({"$inc": {"favorites_count": 1}})
    return favorites


# show all favorites
async def get_all_favorites_crud(user_id: int):
    favorites = await Favorites.find_one(
        Favorites.user_id == user_id
    )
    return favorites


# show one favorite

async def get_one_favorite_crud(user_id: int, property_id: str):
    favorite = await Favorites.find_one(
        Favorites.user_id == user_id,
        Favorites.property_ids == property_id
    )

    return favorite


# delete from favorites
async def delete_favorite_crud(favorite: Favorites, property_id: str):
    await favorite.update({"$pull": {"property_ids": property_id}})
    prop = await get_property_crud(property_id)
    await prop.update({"$inc": {"favorites_count": -1}})
