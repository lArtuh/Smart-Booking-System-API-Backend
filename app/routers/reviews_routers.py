from fastapi import APIRouter, Depends
from app.schemas.reviews_schemas import ReviewResponse, ReviewCreate, ReviewUpdate
from app.models.sql.user_models import User
from app.auth.dependencies import get_current_property, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session
from app.services.review_services import (
    create_review_service,
    show_all_propertys_reviews_service,
    update_review_service
)

review_router = APIRouter(prefix="/reviews", tags=["reviews"])


# create review

@review_router.post("/reviews/{booking_id}/", response_model=ReviewResponse)
async def create_review(
    booking_id: str,
    data: ReviewCreate,
    db: AsyncSession = Depends(async_session),
    current_user: User = Depends(get_current_user),
):
    review = await create_review_service(
        booking_id,
        current_user.id,
        data,
        db
    )
    return review

# # show review
# @review_router.get("/{review_id}", response_model=ReviewResponse)
# async def show_review_router(
#     review_id: str,
#     current_user: User = Depends(get_current_user)
# ):
#     return await show_review(review_id, current_user.id)


# show all reviews
@review_router.get("/", response_model=list[ReviewResponse])
async def show_all_reviews_router(
    property_id: int = Depends(get_current_property),

):
    reviews = await show_all_propertys_reviews_service(property_id)
    return reviews


# update review
@review_router.put("/{review_id}")
async def update_review_router(
    review_id: str,
    data: ReviewUpdate,
    property_id:  int = Depends(get_current_property),
    user_id: int = Depends(get_current_user),
):
    return await update_review_service(user_id, review_id, property_id, data)

# # delete review


# @review_router.delete("/{review_id}")
# async def delete_review_router(
#     review_id: str,
#     current_user: User = Depends(get_current_user)
# ):
#     return await delete_review(review_id, current_user.id)
