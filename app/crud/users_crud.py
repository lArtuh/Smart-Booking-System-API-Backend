from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sql.user_models import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.auth.hashing import Hash
from sqlalchemy import select
from fastapi import HTTPException


async def create_user(db: AsyncSession, data: UserCreate):
    user_email = await db.execute(select(User).where(User.email == data.email))
    existing_user_email = user_email.scalar_one_or_none()
    if existing_user_email:
        raise HTTPException(
            status_code=409, detail="Email already in use")
    print("PASSWORD:", data.password)
    print("TYPE:", type(data.password))
    print("LEN:", len(data.password))
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


async def get_user_by_id(db: AsyncSession, id: int):
    user = await db.execute(select(User).where(User.id == id))
    result = user.scalar_one_or_none()
    if not result:
        raise HTTPException(
            status_code=404, detail="User not found")
    return result


async def get_user_by_email(db: AsyncSession, email: str):
    user = await db.execute(select(User).where(User.email == email))
    result = user.scalar_one_or_none()
    return result


async def get_all_users(db: AsyncSession):
    user = await db.execute(select(User))
    result = user.scalars().all()
    return result


async def update_user(db: AsyncSession, id: int, data: UserUpdate):
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


async def delete_user(db: AsyncSession, id: int):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"message": "user deleted sucesfully"}
