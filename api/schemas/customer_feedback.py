from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

# base schema for customer feedback
class CustomerFeedbackBase(BaseModel):
    customer_id: int
    feedback_text: str

    @validator("feedback_text")
    def validate_feedback_text(cls, value):
        if not value.strip():
            raise ValueError("feedback text cannot be empty")
        return value

# schema for creating feedback
class CustomerFeedbackCreate(CustomerFeedbackBase):
    pass

# schema for updating feedback
class CustomerFeedbackUpdate(BaseModel):
    feedback_text: Optional[str] = None

# schema for returning feedback data
class CustomerFeedback(CustomerFeedbackBase):
    id: int
    submitted_at: datetime

    class Config:
        orm_mode = True
