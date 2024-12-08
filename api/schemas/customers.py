from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    address: Optional[str] = None

# schema for creating a customer
class CustomerCreate(CustomerBase):
    password: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters long")
        return value

# schema for updating a customer
class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

# schema for returning customer data
class Customer(CustomerBase):
    id: int
    saved_payment: Optional[str]

    class Config:
        orm_mode = True
