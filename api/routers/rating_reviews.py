from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers import rating_reviews as rr_controller
from ..schemas.rating_reviews import RatingReviewCreate, RatingReviewUpdate, RatingReview
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Rating Reviews'],
    prefix="/rating_reviews"
)

@router.post("/", response_model=RatingReview)
def submit_review(request: RatingReviewCreate, db: Session = Depends(get_db)):
    return rr_controller.submit_review(db=db, request=request)


@router.put("/{review_id}", response_model=RatingReview)
def edit_review(review_id: int, request: RatingReviewUpdate, db: Session = Depends(get_db)):
    return rr_controller.edit_review(db=db, review_id=review_id, request=request)
