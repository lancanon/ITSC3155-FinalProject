from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

# base schema for rating reviews
class RatingReviewBase(BaseModel):
    customer_id: int
    order_id: int
    review_text: Optional[str] = None
    rating: float

    @validator("rating")
    def validate_rating(cls, value):
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value

# schema for creating a rating review
class RatingReviewCreate(RatingReviewBase):
    pass

# schema for updating a rating review
class RatingReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    rating: Optional[float] = None

    @validator("rating", always=True)
    def validate_rating(cls, value):
        if value and (value < 1 or value > 5):
            raise ValueError("rating must be between 1 and 5")
        return value

# schema for returning rating review data
class RatingReview(RatingReviewBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
