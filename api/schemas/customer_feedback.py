from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CustomerFeedbackBase(BaseModel):
    customer_id: int
    feedback_text: str

class CustomerFeedbackCreate(CustomerFeedbackBase):
    pass

class CustomerFeedbackUpdate(BaseModel):
    feedback_text: Optional[str] = None

class CustomerFeedback(CustomerFeedbackBase):
    id: int
    submitted_at: datetime

    class Config:
        orm_mode = True
