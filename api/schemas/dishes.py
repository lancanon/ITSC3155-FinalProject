from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DishBase(BaseModel):
    dish_name: str
    price: float
    calories : Optional[int] = None
    category : Optional[str] = None

class DishCreate(DishBase):
    pass


class DishUpdate(BaseModel):
    dish_name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None


class Dish(DishBase):
    id: int

    class ConfigDict:
        from_attributes = True