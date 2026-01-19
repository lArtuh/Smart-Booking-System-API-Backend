from fastapi import APIRouter, Depends
from app.schemas.user_schemas import UserCreate, UserResponse
from app.core.database import get_db
from app.services.user_services import (
    register,
    login,
)


user_router = APIRouter(prefix="/users", tags=["Users"])

# register


@user_router.post("/", response_model=UserResponse)
async def register_user(
    data: UserCreate,
    db=Depends(get_db)
):
    new_user = await register(db, data)
    return new_user


# login
@user_router.post("/", response_model=UserResponse)
async def login_user(
    data: UserCreate,
    db=Depends(get_db)
):
    new_user = await login(db, data.email, data.password)
    return new_user
