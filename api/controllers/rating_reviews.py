from fastapi import Response, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime
from ..models import rating_reviews as rr_model, customers as customer_model, orders as order_model, menu_items as menu_model
from ..schemas.rating_reviews import RatingReviewCreate, RatingReviewUpdate


# Submit a new review
def submit_review(db: Session, request: RatingReviewCreate):
    # Validate customer exists
    customer = db.query(customer_model.Customer).filter(customer_model.Customer.id == request.customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Validate order exists
    order = db.query(order_model.Order).filter(order_model.Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Validate rating
    if request.rating < 1 or request.rating > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be between 1 and 5")

    # Create new review
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
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_review


# Edit an existing review
def edit_review(db: Session, review_id: int, request: RatingReviewUpdate):
    review = db.query(rr_model.RatingReview).filter(rr_model.RatingReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    # Validate rating if provided
    if request.rating and (request.rating < 1 or request.rating > 5):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be between 1 and 5")

    # Apply updates
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)
    review.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(review)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return review


# Fetch a list of all reviews
def get_all_reviews(db: Session):
    try:
        return db.query(rr_model.RatingReview).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
# Delete a review
def delete_review(db: Session, review_id: int):
    """
    Delete a rating review by its ID.
    """
    review = db.query(rr_model.RatingReview).filter(rr_model.RatingReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    try:
        db.delete(review)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return {"message": f"Review with ID {review_id} successfully deleted"}
