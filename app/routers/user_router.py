from fastapi import APIRouter, Depends
from app.schemas.user_schemas import UserCreate, UserResponse, UserUpdate
from app.core.database import get_db
from app.crud.users_crud import (
    create_user,
    get_user_by_id,
    update_user,
    delete_user,
    get_all_users
)


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", response_model=UserResponse)
async def register_user(data: UserCreate, db=Depends(get_db)):
    new_user = await create_user(db, data)
    return new_user


@user_router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, db=Depends(get_db)):
    user = await get_user_by_id(db, id)
    return user


@user_router.get("/", response_model=list[UserResponse])
async def get_all_users_router(db=Depends(get_db)):
    users = await get_all_users(db)
    return users


@user_router.put("/{id}", response_model=UserResponse)
async def update_user_router(id: int, data: UserUpdate, db=Depends(get_db)):
    updated_user = await update_user(db, id, data)
    return updated_user


@user_router.delete("/{id}")
async def delete_user_router(id: int, db=Depends(get_db)):
    deleted_user = await delete_user(db, id)
    return deleted_user
