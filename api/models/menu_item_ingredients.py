from sqlalchemy import Table, Column, Integer, ForeignKey
from ..dependencies.database import Base

# Association table for many-to-many relationship
menu_item_ingredients = Table(
    "menu_item_ingredients",
    Base.metadata,
    Column("menu_item_id", Integer, ForeignKey("menu_items.id"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("resource_management.id"), primary_key=True),
)
