from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sql.user_models import User
from app.models.nosql.property_model import Property
from app.auth.hashing import Hash
from fastapi import HTTPException
from app.auth.jwt_handler import create_access_token
from app.schemas.user_schemas import UserCreate
from app.services.properties_services import show_all_user_properties_services
from app.services.booking_services import show_all_property_bookings_services
from app.crud.users_crud import (
    get_all_users_crud,
    get_user_by_id_crud,
    get_user_by_email_crud,
    create_user_crud,
    delete_user_crud,
    delete_all_user_crud
)

# register/login user


async def register(db: AsyncSession, data: UserCreate):
    existing_user_email = await get_user_by_email_crud(db, data.email)
    if existing_user_email:
        raise HTTPException(
            status_code=409, detail="Email already in use")
    new_user = await create_user_crud(db, data)
    email = new_user.email
    password = data.password
    token = await login(db, email, password)
    return token


# loging user

async def login(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email_crud(db, email)
    if not user or not Hash.verify(user.hashed_password, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
     # GENERAR TOKEN
    access_token = create_access_token({"sub": str(user.id)})

    # DEVOLVER TOKEN
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# get all users
async def get_all_user_service(db: AsyncSession):
    user = await get_all_users_crud(db)
    return user


# delete user
async def delete_user_service(db: AsyncSession, user: User):
    user = await get_user_by_id_crud(db, user.id)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found")

    # buscar todas las propiedades de ese usuario, si no hay devuelve lista vacía
    properties: Property = await show_all_user_properties_services(user.id)
    # verificar que ninguna tenga bookings pendientes(eso se hace buscando los bookings por propiedad en un bucle)
    for prop in properties:
        bookings = await show_all_property_bookings_services(prop.id)
        if not bookings:
            # borrar sus respectivas propiedades
            await
            return await delete_user_crud(db, user)

    # borrar las propiedades


# delete all users
async def delete_all_users_service(db: AsyncSession):
    return await delete_all_user_crud(db)
