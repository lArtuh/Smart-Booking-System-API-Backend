from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.user_services import delete_all_users_service
from app.services.properties_services import delete_all_properties_services
from app.services.booking_services import delete_all_bookings_services
from app.services.payment_services import delete_all_payments_service
from app.services.review_services import delete_all_reviews_services
from app.services.favorites_services import delete_all_favorites_services

from app.crud.users_crud import delete_all_user_crud
from app.crud.properties_crud import delete_all_properties_crud
from app.crud.booking_crud import delete_all_bookings_crud
from app.crud.payments_crud import delete_all_payments_crud
from app.crud.reviews_crud import delete_review_crud
from app.crud.favorites_crud import delete_all_favorites_crud

cleaner_router = APIRouter(prefix="/cleaner", tags=["cleaner"])


# delete all database

@cleaner_router.delete("/")
async def delete_all_db_router(
    db: AsyncSession = Depends(get_db)
):
    await delete_all_user_crud(db)
    await delete_all_properties_crud()
    await delete_all_bookings_crud()
    await delete_all_payments_crud(db)
    await delete_review_crud()
    await delete_all_favorites_crud()
    return {"message": "batabase cleaned successfully"}
