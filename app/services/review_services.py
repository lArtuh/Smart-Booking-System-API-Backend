from sqlalchemy.ext.asyncio import AsyncSession
from app.models.nosql.booking_model import Booking
from app.schemas.reviews_schemas import ReviewCreate, ReviewResponse
from app.services.validators import validate_booking_for_review, validate_payment
from app.models.nosql.review_model import Review
from fastapi import HTTPException
from app.crud.booking_crud import get_booking
from app.crud.reviews_crud import (
    create_review_crud,
    get_review_crud,
    show_all_reviews_crud,
    delete_review_crud
)

# make review


async def create_review_service(
    booking_id: str,
    user_id: int,
    data: ReviewCreate,
    db: AsyncSession,
):
    #  obtener la reserva
    booking: Booking = await get_booking(
        booking_id,
        user_id
    )

    #  validar estado de la reserva
    # await validate_booking_for_review(booking)

    #  validar pago
    await validate_payment(
        booking,
        db,
        user_id,
        property_id=booking.property_id,
    )

    print("Review fields:", Review.model_fields)

    # validar si no hay reservas aún
    review = await Review.find_one(
        Review.user_id == user_id,
        Review.property_id == booking.property_id
    )
    if review:
        raise HTTPException(status_code=409, detail="A review already exists.")

    #  crear review

    review = await create_review_crud(
        property_id=booking.property_id,
        user_id=user_id,
        booking_id=str(booking.id),
        data=data

    )

    return ReviewResponse(
        **{**review.model_dump(), "id": str(review.id)}
    )

# show review


async def show_review_service(review_id: str, user_id: int):
    review = await get_review_crud(review_id, user_id)

    return ReviewResponse(
        **{**review.model_dump(), "id": str(review.id)}
    )

# show all propery review


async def show_all_propertys_reviews_service(
    property_id: str
):
    reviews = await show_all_reviews_crud(property_id)
    return [
        ReviewResponse(
            **{**p.model_dump(),
                "id": str(p.id),
                "property_id": (p.property_id)
               }
        )
        for p in reviews
    ]


# # update a review
# async def update_review_service(
#     user_id: int,
#     review_id: str,
#     property_id: str,
#     data: ReviewUpdate
# ):

#     review = await get_review(review_id, user_id, property_id)

#     reviews = await update_review(review, data)
#     return reviews


# delete review
async def delete_review_service(
    review_id: str,
    user_id: int
):

    review = await get_review_crud(review_id, user_id)
    await delete_review_crud(review)
    return {"mensage": "Review deleted successfully"}
