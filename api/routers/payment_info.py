from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ..controllers.payment_info import (
    create_payment_info,
    read_all_payment_info,
    read_payment_info,
    update_payment_info,
    delete_payment_info,
)
from ..schemas.payment_info import PaymentInformationCreate, PaymentInformationUpdate, PaymentInformation
from ..dependencies.database import get_db

router = APIRouter(
    tags=["payment information"],
    prefix="/payment_info"
)

# create new payment information
@router.post("/", response_model=PaymentInformation)
def create_payment_info_route(request: PaymentInformationCreate, db: Session = Depends(get_db)):
    """
    create a new payment information entry.
    """
    return create_payment_info(db, request)

# retrieve all payment information with optional filters
@router.get("/", response_model=list[PaymentInformation])
def read_all_payment_info_route(order_id: int = None, status: str = None, db: Session = Depends(get_db)):
    """
    Retrieve all payment information, with optional filters by order_id or status.
    """
    results = read_all_payment_info(db)
    if order_id:
        results = [p for p in results if p.order_id == order_id]
    if status:
        results = [p for p in results if p.transaction_status == status]
    return results

@router.get("/{payment_id}", response_model=PaymentInformation)
def read_payment_info_route(payment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve specific payment information by id.
    """
    return read_payment_info(db, payment_id)


# update a specific payment information
@router.put("/{payment_id}", response_model=PaymentInformation)
def update_payment_info_route(payment_id: int, request: PaymentInformationUpdate, db: Session = Depends(get_db)):
    """
    update payment information by id.
    """
    return update_payment_info(db, payment_id, request)

# delete a specific payment information
@router.delete("/{payment_id}")
def delete_payment_info_route(payment_id: int, db: Session = Depends(get_db)):
    """
    delete payment information by id.
    """
    return delete_payment_info(db, payment_id)
