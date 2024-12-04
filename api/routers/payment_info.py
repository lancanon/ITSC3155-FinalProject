from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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
    tags=["Payment Information"],
    prefix="/payment_info"
)

@router.post("/", response_model=PaymentInformation)
def create_payment_info_route(request: PaymentInformationCreate, db: Session = Depends(get_db)):
    return create_payment_info(db, request)


@router.get("/", response_model=list[PaymentInformation])
def read_all_payment_info_route(db: Session = Depends(get_db)):
    return read_all_payment_info(db)


@router.get("/{payment_id}", response_model=PaymentInformation)
def read_payment_info_route(payment_id: int, db: Session = Depends(get_db)):
    return read_payment_info(db, payment_id)


@router.put("/{payment_id}", response_model=PaymentInformation)
def update_payment_info_route(payment_id: int, request: PaymentInformationUpdate, db: Session = Depends(get_db)):
    return update_payment_info(db, payment_id, request)


@router.delete("/{payment_id}")
def delete_payment_info_route(payment_id: int, db: Session = Depends(get_db)):
    return delete_payment_info(db, payment_id)
