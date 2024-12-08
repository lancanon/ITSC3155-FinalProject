from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional

# base schema for promotions
class PromotionBase(BaseModel):
    code: str  # unique promotion code
    description: Optional[str] = None  # optional description of the promotion
    discount_percentage: float  # discount percentage for the promotion
    expiration_date: date  # expiration date for the promotion
    is_active: bool = True  # indicates whether the promotion is active

    @validator("discount_percentage")
    def validate_discount_percentage(cls, value):
        # validate that discount percentage is between 0 and 100
        if value <= 0 or value > 100:
            raise ValueError("discount percentage must be between 0 and 100.")
        return value

    @validator("expiration_date")
    def validate_expiration_date(cls, value):
        # ensure expiration date is in the future
        if value < date.today():
            raise ValueError("expiration date must be in the future.")
        return value

# schema for creating a promotion
class PromotionCreate(PromotionBase):
    pass

# schema for updating a promotion
class PromotionUpdate(BaseModel):
    description: Optional[str] = None
    discount_percentage: Optional[float] = None
    expiration_date: Optional[date] = None
    is_active: Optional[bool] = None

# schema for returning promotion data
# Response schema for returning promotion data
class PromotionResponse(BaseModel):
    id: int  # Unique identifier for the promotion
    code: str  # Promotion code
    description: Optional[str] = None  # Description of the promotion
    discount_percentage: float  # Discount percentage
    expiration_date: date  # Expiration date of the promotion
    is_active: bool  # Whether the promotion is active
    
    class Config:
        orm_mode = True
