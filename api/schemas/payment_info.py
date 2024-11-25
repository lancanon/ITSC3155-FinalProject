from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentInformationBase(BaseModel):
    order_id: int
    payment_type: str
    transaction_status: str
    card_number: Optional[str] = None

class PaymentInformationCreate(PaymentInformationBase):
    pass

class PaymentInformationUpdate(BaseModel):
    payment_type: Optional[str] = None
    transaction_status: Optional[str] = None
    card_number: Optional[str] = None

class PaymentInformation(PaymentInformationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
