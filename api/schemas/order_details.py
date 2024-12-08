from pydantic import BaseModel, validator
from .menu_items import MenuItem  # Import the Pydantic model for MenuItem
from typing import Optional

# base schema for order details
class OrderDetailBase(BaseModel):
    quantity: int

    @validator("quantity")
    def validate_quantity(cls, value):
        # ensure quantity is greater than zero
        if value <= 0:
            raise ValueError("quantity must be greater than zero")
        return value

# schema for creating an order detail
class OrderDetailCreate(OrderDetailBase):
    order_id: int
    menu_item_id: int

# schema for updating an order detail
class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    quantity: Optional[int] = None

# schema for returning order detail data
class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    menu_item: MenuItem  

    class Config:
        orm_mode = True
