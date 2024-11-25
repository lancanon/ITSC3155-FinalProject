from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    ingredients = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    calories = Column(Integer, nullable=True)
    menu_category = Column(String(50), nullable=False)  
    dietary_category = Column(String(50), nullable=True)
    available = Column(Boolean, default=True, nullable=False)

    # Relationships
    order_details = relationship("OrderDetail", back_populates="menu_item")
    recipes = relationship("Recipe", back_populates="menu_item")
