from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .dishes import Dish


class OrderDetailBase(BaseModel):
    amount: int


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    dish_id: int

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    dish_id: Optional[int] = None
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    dish: Dish = None

    class ConfigDict:
        from_attributes = True