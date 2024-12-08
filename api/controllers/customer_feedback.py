from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from ..models.customer_feedback import CustomerFeedback
from ..models.customers import Customer
from ..schemas.customer_feedback import CustomerFeedbackCreate, CustomerFeedbackUpdate


def create_feedback(db: Session, request: CustomerFeedbackCreate):
    # validate customer exists
    customer = db.query(Customer).filter(Customer.id == request.customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="customer not found")

    # create new feedback
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
        # fetch all feedbacks with customer details
        return db.query(CustomerFeedback).options(joinedload(CustomerFeedback.customer)).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_feedback(db: Session, feedback_id: int):
    feedback = db.query(CustomerFeedback).options(joinedload(CustomerFeedback.customer)).filter(CustomerFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="feedback not found")
    return feedback


def update_feedback(db: Session, feedback_id: int, request: CustomerFeedbackUpdate):
    feedback = db.query(CustomerFeedback).filter(CustomerFeedback.id == feedback_id)
    if not feedback.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="feedback not found")

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="feedback not found")

    try:
        feedback.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return {"message": "feedback deleted successfully"}
