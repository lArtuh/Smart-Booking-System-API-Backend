from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.hashing import Hash
from fastapi import HTTPException
from app.auth.jwt_handler import create_access_token
from app.schemas.user_schemas import UserCreate
from app.crud.users_crud import (
    get_all_users,
    get_user_by_email,
    create_user
)

# registrar usuario


async def register(db: AsyncSession, data: UserCreate):
    new_user = await create_user(db, data)
    email = new_user.email
    password = data.password
    token = await login(db, email, password)
    return token
# logear usuario


async def login(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not Hash.verify(user.hashed_password, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
     # GENERAR TOKEN
    access_token = create_access_token({"sub": str(user.id)})

    # DEVOLVER TOKEN
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# get user by email
async def get_user_by_email_service(db: AsyncSession, email: str):
    user = await get_user_by_email(db, email)
    return user


# get all users
async def get_all_user_service(db: AsyncSession):
    user = await get_all_users(db)
    return user
