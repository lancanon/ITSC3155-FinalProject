from sqlalchemy import Column, ForeignKey, Integer, String, Float, Enum, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    customer_name = Column(String(100), nullable=False)
    description = Column(String(256), nullable=True)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    tracking_number = Column(String(100), unique=True, nullable=False)
    status = Column(Enum("Pending", "Preparing", "Delivered", "Cancelled", name="order_status"), nullable=False, default="Pending")
    order_type = Column(Enum("Takeout", "Delivery", name="order_type_enum"), nullable=False, default="Takeout")  # new field for type of order
    total_price = Column(Float, nullable=False)
    payment_status = Column(String(20), default="Pending")  # New field for payment status
    payment_method = Column(String(50), nullable=True)  # New field for payment method

    # relationships
    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    ratings_reviews = relationship("RatingReview", back_populates="order", uselist=False)
    payment_info = relationship("PaymentInformation", back_populates="order", uselist=False)

    # index for frequent queries
    __table_args__ = (
        Index("idx_order_status", "status"),
        Index("idx_order_date", "order_date"),
    )
