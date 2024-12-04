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
    tags=["Customer Feedback"],
    prefix="/customer_feedback"
)

@router.post("/", response_model=CustomerFeedback)
def create_feedback_route(request: CustomerFeedbackCreate, db: Session = Depends(get_db)):
    return create_feedback(db, request)


@router.get("/", response_model=list[CustomerFeedback])
def read_all_feedbacks_route(db: Session = Depends(get_db)):
    return read_all_feedbacks(db)


@router.get("/{feedback_id}", response_model=CustomerFeedback)
def read_feedback_route(feedback_id: int, db: Session = Depends(get_db)):
    return read_feedback(db, feedback_id)


@router.put("/{feedback_id}", response_model=CustomerFeedback)
def update_feedback_route(feedback_id: int, request: CustomerFeedbackUpdate, db: Session = Depends(get_db)):
    return update_feedback(db, feedback_id, request)


@router.delete("/{feedback_id}")
def delete_feedback_route(feedback_id: int, db: Session = Depends(get_db)):
    return delete_feedback(db, feedback_id)
