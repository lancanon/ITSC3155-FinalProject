from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dish_name = Column(String(100), unique=True, nullable=True)
    price = Column(DECIMAL(4, 2), nullable=False, server_default='0.0')
    category = Column(String(100), unique=False, nullable=True)
    calories = Column(Integer, unique=False, nullable=True)

    recipes = relationship("Recipe", back_populates="dishes")
    order_details = relationship("OrderDetail", back_populates="dishes")
