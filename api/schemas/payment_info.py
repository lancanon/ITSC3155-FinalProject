from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base schema for shared fields
class PaymentInformationBase(BaseModel):
    order_id: int
    payment_type: str  # Example: "Credit Card", "PayPal", etc.
    transaction_status: str  # Example: "Pending", "Completed", "Failed"

# Schema for creating a new payment info entry
class PaymentInformationCreate(PaymentInformationBase):
    pass  # No additional fields required for creation

# Schema for updating payment info
class PaymentInformationUpdate(BaseModel):
    payment_type: Optional[str] = None  # Allow updating the payment method
    transaction_status: Optional[str] = None  # Allow updating the transaction status

# Schema for returning payment info data
class PaymentInformation(PaymentInformationBase):
    id: int  # Primary key ID of the payment info
    created_at: datetime  # Timestamp when the payment info was created

    class Config:
        orm_mode = True  # Enable ORM compatibility
