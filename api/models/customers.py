from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)
    address = Column(Text, nullable=True)
    password_hash = Column(String(256), nullable=False)
    saved_payment = Column(String(50), nullable=True)

    # relationships
    orders = relationship("Order", back_populates="customer")
    ratings_reviews = relationship("RatingReview", back_populates="customer")
    feedback = relationship("CustomerFeedback", back_populates="customer")
