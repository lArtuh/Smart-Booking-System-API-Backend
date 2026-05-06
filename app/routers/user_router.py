from app.auth.dependencies import get_current_user
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.sql.user_models import User
from app.schemas.user_schemas import UserCreate, UserResponse, Token, UserLogin
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_services import (
    register,
    login,
    get_all_user_service,
    delete_user_service,
    delete_all_users_service
)


user_router = APIRouter(prefix="/users", tags=["Users"])

# register


@user_router.post("/register", response_model=Token)
async def register_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    new_user = await register(db, data)
    return new_user


login


@user_router.post("/login", response_model=Token)
async def login_user(
    data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    new_user = await login(db, data.email, data.password)
    return new_user


# # loginForm
# @user_router.post("/login", response_model=Token)
# async def login_user(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: AsyncSession = Depends(get_db)
# ):
#     new_user = await login(db, form_data.username, form_data.password)
#     return new_user


# get users


@user_router.get("/all", response_model=list[UserResponse])
async def get_users_router(
    db: AsyncSession = Depends(get_db)
):
    users: list = await get_all_user_service(db)
    return users


# delete User
@user_router.delete("/delete")
async def delete_user_router(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_user_service(db, current_user)


# delete all Users
@user_router.delete("/deleteall")
async def delete_all_user_router(
    db: AsyncSession = Depends(get_db)
):
    return await delete_all_users_service(db)
