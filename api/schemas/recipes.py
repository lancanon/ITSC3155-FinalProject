from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource
from .dishes import Dish


class RecipeBase(BaseModel):
    amount: int


class RecipeCreate(RecipeBase):
    dish_id: int
    resource_id: int

class RecipeUpdate(BaseModel):
    dish_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    dish: Dish = None
    resource: Resource = None

    class ConfigDict:
        from_attributes = True