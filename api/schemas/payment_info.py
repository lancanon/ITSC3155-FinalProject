from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class PaymentInformationBase(BaseModel):
    order_id: int
    payment_type: str
    transaction_status: str
    card_number: Optional[str] = None

    @validator("transaction_status")
    def validate_transaction_status(cls, value):
        if value not in ["Pending", "Completed", "Failed"]:
            raise ValueError("invalid transaction status. must be 'Pending', 'Completed', or 'Failed'")
        return value

    @validator("card_number")
    def validate_card_number(cls, value):
        if value and (not value.isdigit() or len(value) != 16):
            raise ValueError("invalid card number. must be 16 digits")
        return value

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
