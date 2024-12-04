from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.customer_feedback import CustomerFeedback
from ..schemas.customer_feedback import CustomerFeedbackCreate, CustomerFeedbackUpdate


def create_feedback(db: Session, request: CustomerFeedbackCreate):
    feedback = CustomerFeedback(
        customer_id=request.customer_id,
        feedback_text=request.feedback_text
    )
    try:
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return feedback


def read_all_feedbacks(db: Session):
    try:
        return db.query(CustomerFeedback).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_feedback(db: Session, feedback_id: int):
    feedback = db.query(CustomerFeedback).filter(CustomerFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return feedback


def update_feedback(db: Session, feedback_id: int, request: CustomerFeedbackUpdate):
    feedback = db.query(CustomerFeedback).filter(CustomerFeedback.id == feedback_id)
    if not feedback.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

    update_data = request.dict(exclude_unset=True)
    try:
        feedback.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return feedback.first()


def delete_feedback(db: Session, feedback_id: int):
    feedback = db.query(CustomerFeedback).filter(CustomerFeedback.id == feedback_id)
    if not feedback.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")

    try:
        feedback.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return {"message": "Feedback deleted successfully"}
