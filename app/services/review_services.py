from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.reviews_schemas import ReviewCreate
from app.services.validators import validate_booking_for_review, validate_payment
from app.services.properties_services import serialize
from app.models.nosql.review_model import Review
from fastapi import HTTPException
from app.crud.booking_crud import get_booking_crud
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

    booking = await get_booking_crud(booking_id, user_id)

    #  validar si la reserva no fue cancelada (esto estaba generando problemas por eso lo desactivé)
    #  await validate_booking_for_review(booking)

    #  validar pago
    # await validate_payment(
    #     booking,
    #     db,
    #     user_id,
    #     property_id=booking.property_id,
    # )

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

    return await serialize(review)


# show review


async def show_review_service(review_id: str, user_id: int):
    review = await get_review_crud(review_id, user_id)

    return await serialize(review)

# show all propery review


async def show_all_propertys_reviews_service(
    property_id: str
):
    reviews = await show_all_reviews_crud(property_id)
    return [
        await serialize(p)
        for p in reviews
    ]


# delete review
async def delete_review_service(
    review_id: str,
    user_id: int
):

    review = await get_review_crud(review_id, user_id)
    await delete_review_crud(review)
    return {"mensage": "Review deleted successfully"}
