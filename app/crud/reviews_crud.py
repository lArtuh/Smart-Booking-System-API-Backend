from app.models.nosql.review_model import Review
from app.schemas.reviews_schemas import ReviewCreate
from fastapi import HTTPException
from beanie import PydanticObjectId

# create review


async def create_review_crud(
    property_id: str,
    user_id: int,
    booking_id: str,
    data: ReviewCreate,
):
    new_review = Review(
        **data.model_dump(),
        property_id=property_id,
        booking_id=booking_id,
        user_id=user_id,
    )

    await new_review.insert()
    return new_review


# show review


async def get_review_crud(review_id: str, user_id: int):
    try:
        review_oid = PydanticObjectId(review_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    review = await Review.find_one(
        Review.id == review_oid,
        Review.user_id == user_id
    )
    if not review:
        raise HTTPException(status_code=404, detail="not found")
    return review


# show all reviews by property

async def show_all_reviews_crud(property_id: str):

    reviews = await Review.find(Review.property_id == property_id).to_list()
    return reviews


# delete review


async def delete_review_crud(review: Review):
    await review.delete()


# delete all reviews

async def delete_all_reviews_crud():
    await Review.find_all().delete()
