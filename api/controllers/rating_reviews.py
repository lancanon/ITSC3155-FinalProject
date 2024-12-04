from fastapi import Response, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import rating_reviews as rr_model
from datetime import datetime
from ..schemas.rating_reviews import RatingReviewCreate, RatingReviewUpdate


def submit_review(db: Session, request: RatingReviewCreate):
    if request.rating < 1 or request.rating > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be between 1 and 5.")

    new_review = rr_model.RatingReview(
        customer_id=request.customer_id,
        order_id=request.order_id,
        review_text=request.review_text,
        rating=request.rating,
        created_at=datetime.utcnow()
    )
    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return new_review


def edit_review(db: Session, review_id: int, request: RatingReviewUpdate):
    review = db.query(rr_model.RatingReview).filter(rr_model.RatingReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found!")

    if request.rating and (request.rating < 1 or request.rating > 5):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be between 1 and 5.")
    
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)
    review.created_at = datetime.utcnow()  # Update timestamp
    
    try:
        db.commit()
        db.refresh(review)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return review
