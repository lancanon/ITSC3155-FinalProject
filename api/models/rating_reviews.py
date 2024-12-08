from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class RatingReview(Base):
    __tablename__ = "ratings_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    review_text = Column(Text, nullable=True)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.utcnow)  # auto-update field

    # relationships
    customer = relationship("Customer", back_populates="ratings_reviews")
    order = relationship("Order", back_populates="ratings_reviews")

    # indices for optimization
    __table_args__ = (
        Index("idx_customer_id", "customer_id"),
        Index("idx_order_id", "order_id"),
    )
