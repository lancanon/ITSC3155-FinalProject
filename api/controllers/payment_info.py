from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.payment_info import PaymentInformation
from typing import Optional
from ..schemas.payment_info import PaymentInformationCreate, PaymentInformationUpdate
from sqlalchemy.exc import SQLAlchemyError


def read_all_payment_info(
    db: Session,
    order_id: Optional[int] = None,
    transaction_status: Optional[str] = None
):
    try:
        query = db.query(PaymentInformation)

        # Apply filters if provided
        if order_id:
            query = query.filter(PaymentInformation.order_id == order_id)
        if transaction_status:
            query = query.filter(PaymentInformation.transaction_status == transaction_status)

        # Execute query
        payment_info_list = query.all()
        return payment_info_list
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )
    
# Create new payment info
def create_payment_info(db: Session, request: PaymentInformationCreate):
    new_payment = PaymentInformation(
        order_id=request.order_id,
        payment_type=request.payment_type,
        transaction_status=request.transaction_status,
    )
    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return new_payment
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Get all payment info with optional filters
def get_all_payment_info(db: Session, order_id: Optional[int] = None, status: Optional[str] = None):
    query = db.query(PaymentInformation)
    if order_id:
        query = query.filter(PaymentInformation.order_id == order_id)
    if status:
        query = query.filter(PaymentInformation.transaction_status == status)
    return query.all()

# Get a specific payment info by ID
def get_payment_info(db: Session, payment_id: int):
    payment = db.query(PaymentInformation).filter(PaymentInformation.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment information not found")
    return payment

# Update payment info by ID
def update_payment_info(db: Session, payment_id: int, request: PaymentInformationUpdate):
    payment = db.query(PaymentInformation).filter(PaymentInformation.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment information not found")
    
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(payment, key, value)
    
    try:
        db.commit()
        db.refresh(payment)
        return payment
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Delete payment info by ID
def delete_payment_info(db: Session, payment_id: int):
    payment = db.query(PaymentInformation).filter(PaymentInformation.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment information not found")
    try:
        db.delete(payment)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
