from sqlalchemy import Column, ForeignKey, Integer, Float, Index
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)  # Quantity of the menu item in the order
    price = Column(Float, nullable=False)  # Total price for the item in the order

    # Relationships
    order = relationship("Order", back_populates="order_details")
    menu_item = relationship("MenuItem", back_populates="order_details")

    # Index definitions
    __table_args__ = (
        Index("idx_order_id", "order_id"),
        Index("idx_menu_item_id", "menu_item_id"),
    )
