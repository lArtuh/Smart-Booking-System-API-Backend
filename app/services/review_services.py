from sqlalchemy.ext.asyncio import AsyncSession
from app.models.nosql.booking_model import Booking
from app.schemas.reviews_schemas import ReviewCreate, ReviewUpdate
from app.crud.booking_crud import get_booking
from app.services.validators import validate_booking_for_review, validate_payment
from app.crud.reviews_crud import (
    create_review,
    get_review,
    show_all_reviews,
    update_review,
    delete_review
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
    validate_booking_for_review(booking)

    #  validar pago
    await validate_payment(
        booking_id,
        db,
        user_id,
        property_id=booking.property_id,
    )

    #  crear review
    review = await create_review(
        property_id=booking.property_id,
        user_id=user_id,
        data=data,
    )

    return review


# show all propery review

async def show_all_propertys_reviews_service(
    property_id: str,
):
    reviews = show_all_reviews(property_id)
    return reviews


# update a review
async def update_review_service(
    user_id: int,
    review_id: str,
    property_id: str,
    data: ReviewUpdate
):

    review = await get_review(review_id, user_id, property_id)

    reviews = update_review(review, data)
    return reviews


# delete review
async def delete_review_service(
    user_id: int,
    review_id: str,
    property_id: str,
):

    review = await get_review(review_id, user_id, property_id)
    deleted_review = delete_review(review)
    return await deleted_review
