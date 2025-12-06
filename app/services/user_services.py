from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.hashing import Hash
from fastapi import HTTPException
from app.crud.users_crud import get_user_by_email
from app.auth.jwt_handler import create_access_token


async def login(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not Hash.verify(user.hashed_password, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
     # GENERAR TOKEN
    access_token = create_access_token({"sub": str(user.id)})

    # DEVOLVER TOKEN
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
