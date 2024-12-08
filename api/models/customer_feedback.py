from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class CustomerFeedback(Base):
    __tablename__ = "customer_feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    feedback_text = Column(Text, nullable=False)
    submitted_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # relationships
    customer = relationship("Customer", back_populates="feedback")

    # index for customer_id
    __table_args__ = (
        Index("idx_customer_id", "customer_id"),
    )
