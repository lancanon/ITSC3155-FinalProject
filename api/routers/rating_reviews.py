from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..controllers import rating_reviews as rr_controller
from ..schemas.rating_reviews import RatingReviewCreate, RatingReviewUpdate, RatingReview
from ..dependencies.database import get_db

router = APIRouter(
    tags=["rating reviews"],
    prefix="/rating_reviews"
)

# Submit a new review
@router.post("/", response_model=RatingReview)
def submit_review(request: RatingReviewCreate, db: Session = Depends(get_db)):
    """
    Submit a new rating review.
    """
    return rr_controller.submit_review(db=db, request=request)


# Edit an existing review
@router.put("/{review_id}", response_model=RatingReview)
def edit_review(review_id: int, request: RatingReviewUpdate, db: Session = Depends(get_db)):
    """
    Edit an existing rating review.
    """
    return rr_controller.edit_review(db=db, review_id=review_id, request=request)

# Fetch a list of all reviews
@router.get("/", response_model=List[RatingReview])
def get_all_reviews(db: Session = Depends(get_db)):
    """
    Fetch a list of all reviews.
    """
    return rr_controller.get_all_reviews(db=db)