from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship
from ..models.menu_item_ingredients import menu_item_ingredients
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    calories = Column(Integer, nullable=True)
    menu_category = Column(String(50), nullable=False, index=True)
    dietary_category = Column(String(50), nullable=True)
    available = Column(Boolean, default=True, nullable=False, index=True)

    # Relationships
    resources = relationship(
        "ResourceManagement",
        secondary=menu_item_ingredients,
        back_populates="menu_items"
    )
    order_details = relationship("OrderDetail", back_populates="menu_item")

    @property
    def ingredients(self):
        """
        Returns a dictionary of ingredient names and their required quantities.
        This aggregates data from the `resources` relationship.
        """
        return {resource.ingredient_name: resource.current_amount for resource in self.resources}

    def __repr__(self):
        return f"<MenuItem(name={self.name}, price={self.price}, available={self.available})>"
