from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resource_management.id"), nullable=False)
    quantity = Column(Float, nullable=False, server_default="0.0")

    # relationships
    menu_item = relationship("MenuItem", back_populates="recipes")
    resource = relationship("ResourceManagement", back_populates="recipes")