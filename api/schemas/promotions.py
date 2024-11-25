from pydantic import BaseModel
from datetime import date
from typing import Optional

class PromotionBase(BaseModel):
    code: str
    description: Optional[str] = None
    discount_percentage: float
    expiration_date: date
    is_active: bool = True

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    description: Optional[str] = None
    discount_percentage: Optional[float] = None
    expiration_date: Optional[date] = None
    is_active: Optional[bool] = None

class Promotion(PromotionBase):
    id: int

    class Config:
        orm_mode = True
