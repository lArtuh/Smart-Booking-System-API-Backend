from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sql.user_models import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.auth.hashing import Hash
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy import delete


async def create_user_crud(db: AsyncSession, data: UserCreate):
    hashed_pw = Hash.bcrypt(data.password)
    new_user = User(
        name=data.name,
        email=data.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_id_crud(db: AsyncSession, id: int):
    user = await db.execute(select(User).where(User.id == id))
    result = user.scalar_one_or_none()
    return result


async def get_user_by_email_crud(db: AsyncSession, email: str):
    user = await db.execute(select(User).where(User.email == email))
    result = user.scalar_one_or_none()
    return result


async def get_all_users_crud(db: AsyncSession):
    user = await db.execute(select(User))
    result = user.scalars().all()
    return result


async def update_user_crud(db: AsyncSession, id: int, data: UserUpdate):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()

    update_data = data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = Hash.bcrypt(
            update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_crud(db: AsyncSession, user: User):
    await db.delete(user)
    await db.commit()
    return {"message": "user deleted sucesfully"}


async def delete_all_user_crud(db: AsyncSession):
    await db.execute(delete(User))
    await db.commit()
    return {"message": "All users deleted sucesfully"}
