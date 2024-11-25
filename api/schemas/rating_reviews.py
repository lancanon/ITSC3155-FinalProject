from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RatingReviewBase(BaseModel):
    customer_id: int
    order_id: int
    review_text: Optional[str] = None
    rating: float

class RatingReviewCreate(RatingReviewBase):
    pass

class RatingReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    rating: Optional[float] = None

class RatingReview(RatingReviewBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
