from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class RatingReview(Base):
    __tablename__ = "ratings_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    review_text = Column(Text, nullable=True)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # relationships
    customer = relationship("Customer", back_populates="ratings_reviews")
    order = relationship("Order", back_populates="ratings_reviews")
