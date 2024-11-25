from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class ResourceManagement(Base):
    __tablename__ = "resource_management"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ingredient_name = Column(String(100), nullable=False, unique=True)
    current_amount = Column(Float, nullable=False, default=0.0)
    unit = Column(String(20), nullable=False)
    threshold_level = Column(Float, nullable=False)

    # Relationships
    recipes = relationship("Recipe", back_populates="resource")
