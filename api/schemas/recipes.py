from pydantic import BaseModel
from typing import Optional
from .resource_management import ResourceManagement
from .menu_items import MenuItem


class RecipeBase(BaseModel):
    quantity: int


class RecipeCreate(RecipeBase):
    menu_item_id: int
    resource_id: int

class RecipeUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    resource_id: Optional[int] = None
    quantity: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    menu_item: MenuItem = None
    resource: ResourceManagement = None

    class ConfigDict:
        from_attributes = True