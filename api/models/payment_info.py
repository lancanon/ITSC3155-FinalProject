from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class PaymentInformation(Base):
    __tablename__ = "payment_information"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    payment_type = Column(String(50), nullable=False)
    card_number = Column(String(16), nullable=True)  # ensure card numbers are max 16 digits
    transaction_status = Column(
        Enum("Pending", "Completed", "Failed", name="transaction_status_enum"),
        nullable=False,
        default="Pending"
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # relationships
    order = relationship("Order", back_populates="payment_info")

    # add index for better performance
    __table_args__ = (
        Index("idx_order_id", "order_id"),
    )
