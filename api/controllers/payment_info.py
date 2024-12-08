from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models.payment_info import PaymentInformation
from ..models.orders import Order
from typing import Optional
from ..schemas.payment_info import PaymentInformationCreate, PaymentInformationUpdate

def create_payment_info(db: Session, request: PaymentInformationCreate):
    # validate order_id exists
    order = db.query(Order).filter(Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")

    # validate transaction_status
    if request.transaction_status not in ["Pending", "Completed", "Failed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid transaction status. must be 'Pending', 'Completed', or 'Failed'"
        )

    # create new payment information
    payment_info = PaymentInformation(
        order_id=request.order_id,
        payment_type=request.payment_type,
        card_number=request.card_number,
        transaction_status=request.transaction_status,
    )
    try:
        db.add(payment_info)
        db.commit()
        db.refresh(payment_info)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return payment_info

def read_all_payment_info(db: Session):
    try:
        # Query all payment information without masking the card number
        payment_infos = db.query(PaymentInformation).all()
        return payment_infos
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_payment_info(db: Session, payment_id: int):
    payment_info = db.query(PaymentInformation).filter(PaymentInformation.id == payment_id).first()
    if not payment_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment info not found")
    # Return the payment info as is
    return payment_info


def update_payment_info(db: Session, payment_id: int, request: PaymentInformationUpdate):
    payment_info = db.query(PaymentInformation).filter(PaymentInformation.id == payment_id)
    if not payment_info.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="payment info not found")

    # validate transaction_status if provided
    if request.transaction_status and request.transaction_status not in ["Pending", "Completed", "Failed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid transaction status. must be 'Pending', 'Completed', or 'Failed'"
        )

    # apply updates
    update_data = request.dict(exclude_unset=True)
    try:
        payment_info.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return payment_info.first()

def delete_payment_info(db: Session, payment_id: int):
    payment_info = db.query(PaymentInformation).filter(PaymentInformation.id == payment_id)
    if not payment_info.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="payment info not found")

    try:
        payment_info.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return {"message": "payment info deleted successfully"}
