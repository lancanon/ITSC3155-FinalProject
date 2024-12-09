from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..dependencies.database import get_db
from ..controllers.payment_info import (
    create_payment_info,
    read_all_payment_info,
    get_payment_info,
    update_payment_info,
    delete_payment_info
)
from ..schemas.payment_info import PaymentInformationCreate, PaymentInformationUpdate, PaymentInformation

router = APIRouter(
    prefix="/payment_info",
    tags=["Payment Information"],
)

# Create a new payment information entry
@router.post("/", response_model=PaymentInformation, status_code=status.HTTP_201_CREATED)
def create_payment_info_route(request: PaymentInformationCreate, db: Session = Depends(get_db)):
    """
    Create a new payment information record.
    """
    return create_payment_info(db, request)

# Get all payment information
@router.get("/", response_model=List[PaymentInformation])
def get_all_payment_info_route(
    order_id: Optional[int] = None,
    transaction_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all payment information, optionally filtered by order ID or transaction status.
    """
    return read_all_payment_info(db, order_id, transaction_status)

# Get payment information by ID
@router.get("/{payment_id}", response_model=PaymentInformation)
def get_payment_info_route(payment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve payment information by ID.
    """
    return get_payment_info(db, payment_id)

# Update payment information by ID
@router.put("/{payment_id}", response_model=PaymentInformation)
def update_payment_info_route(payment_id: int, request: PaymentInformationUpdate, db: Session = Depends(get_db)):
    """
    Update payment information for a specific payment ID.
    """
    return update_payment_info(db, payment_id, request)

# Delete payment information by ID
@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment_info_route(payment_id: int, db: Session = Depends(get_db)):
    """
    Delete payment information by ID.
    """
    return delete_payment_info(db, payment_id)
