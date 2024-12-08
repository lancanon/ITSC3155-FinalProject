from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers.customer_feedback import (
    create_feedback,
    read_all_feedbacks,
    read_feedback,
    update_feedback,
    delete_feedback,
)
from ..schemas.customer_feedback import CustomerFeedbackCreate, CustomerFeedbackUpdate, CustomerFeedback
from ..dependencies.database import get_db

router = APIRouter(
    tags=["customer feedback"],
    prefix="/customer_feedback"
)

# create a new feedback
@router.post("/", response_model=CustomerFeedback)
def create_feedback_route(request: CustomerFeedbackCreate, db: Session = Depends(get_db)):
    """
    create a new customer feedback.
    """
    return create_feedback(db, request)

# retrieve all feedbacks with optional filtering
@router.get("/", response_model=list[CustomerFeedback])
def read_all_feedbacks_route(customer_id: int = None, db: Session = Depends(get_db)):
    """
    retrieve all customer feedbacks, optionally filtered by customer_id.
    """
    feedbacks = read_all_feedbacks(db)
    if customer_id:
        feedbacks = [f for f in feedbacks if f.customer_id == customer_id]
    return feedbacks

# retrieve a specific feedback by id
@router.get("/{feedback_id}", response_model=CustomerFeedback)
def read_feedback_route(feedback_id: int, db: Session = Depends(get_db)):
    """
    retrieve a specific feedback by id.
    """
    return read_feedback(db, feedback_id)

# update a specific feedback
@router.put("/{feedback_id}", response_model=CustomerFeedback)
def update_feedback_route(feedback_id: int, request: CustomerFeedbackUpdate, db: Session = Depends(get_db)):
    """
    update an existing feedback by id.
    """
    return update_feedback(db, feedback_id, request)

# delete a specific feedback
@router.delete("/{feedback_id}")
def delete_feedback_route(feedback_id: int, db: Session = Depends(get_db)):
    """
    delete a customer feedback by id.
    """
    return delete_feedback(db, feedback_id)
