from fastapi import APIRouter, Depends
from app.schemas.user_schemas import UserCreate, UserResponse, Token, UserLogin
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_services import (
    register,
    login,
    get_all_user_service
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


# login
@user_router.post("/login", response_model=Token)
async def login_user(
    data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    new_user = await login(db, data.email, data.password)
    return new_user

# delogin


@user_router.get("/all", response_model=list[UserResponse])
async def delogin(
    db: AsyncSession = Depends(get_db)
):
    users: list = await get_all_user_service(db)
    return users

# get users


@user_router.get("/all", response_model=list[UserResponse])
async def get_users_router(
    db: AsyncSession = Depends(get_db)
):
    users: list = await get_all_user_service(db)
    return users
