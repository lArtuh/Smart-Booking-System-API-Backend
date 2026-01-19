from app.models.nosql.review_model import Review
from app.schemas.reviews_schemas import ReviewCreate, ReviewUpdate
from fastapi import HTTPException

# create review


async def create_review(
    property_id: str,
    user_id: int,
    data: ReviewCreate,
):
    new_review = Review(**data.model_dump())
    new_review.property_id = property_id
    new_review.user_id = user_id

    await new_review.insert()
    return new_review


# show review


async def get_review(review_id: str, user_id: str, property_id: str):
    review = await Review.find_one(
        (Review.id == review_id) &
        (Review.user_id == user_id) &
        (Review.property_id == property_id)
    )
    if not review:
        raise HTTPException(status_code=404, detail="not found")
    return review


# show all reviews by property

async def show_all_reviews(property_id: str):
    reviews = await Review.find(Review.property_id == property_id).to_list()
    return reviews


# update review
async def update_review(review: Review, data: ReviewUpdate):
    await review.set(data.model_dump(exclude_unset=True))
    return {"message": "Review updated successfully"}

# delete review


async def delete_review(review: Review):
    await review.delete()
    return {"mensage": "Review deleted successfully"}
