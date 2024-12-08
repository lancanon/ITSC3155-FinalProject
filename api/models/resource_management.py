from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class ResourceManagement(Base):
    __tablename__ = "resource_management"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ingredient_name = Column(String(100), nullable=False, unique=True)
    current_amount = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    threshold_level = Column(Float, nullable=False)

    # Relationship with Menu Items
    menu_items = relationship(
        "MenuItem",
        secondary="menu_item_ingredients",
        back_populates="resources"
    )

    def __repr__(self):
        return f"<ResourceManagement(name={self.ingredient_name}, current_amount={self.current_amount}, unit={self.unit})>"
