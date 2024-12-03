from sqlalchemy import Column, ForeignKey, Integer, String, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer_name= Column(String(100), nullable=False)
    description = Column(String(256), nullable=True)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    tracking_number = Column(String(100), unique=True, nullable=False)
    status = Column(Enum("Pending", "Preparing", "Delivered", name="order_status"), nullable=False, default="Pending")
    total_price = Column(Float, nullable=False)

    # relationships
    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    ratings_reviews = relationship("RatingReview", back_populates="order", uselist=False)
    payment_info = relationship("PaymentInformation", back_populates="order", uselist=False)

