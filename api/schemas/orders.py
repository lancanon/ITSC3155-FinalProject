from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from .order_details import OrderDetail  # Make sure this import is correct

# Define the OrderItemCreate class (Make sure it's above OrderCreate)
class OrderItemCreate(BaseModel):
    menu_item_id: int  # ID of the menu item selected
    quantity: int  # Quantity of the selected menu item

    class Config:
        orm_mode = True


# Base Order schema shared by both account and guest orders
class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    tracking_number: str  # Tracking number is included but will be auto-generated
    total_price: float  # Adding the total price

# OrderCreate schema uses OrderItemCreate
class OrderCreate(BaseModel):
    customer_name: str
    email: EmailStr  # Email is required to identify the guest or existing customer
    phone_number: Optional[str] = None  # Optional for guest orders
    address: Optional[str] = None  # Optional, but often necessary for guest orders
    menu_items: List[OrderItemCreate]  # List of menu items with quantity and menu_item_id

# Order update schema for modifying an existing order
class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    tracking_number: Optional[str] = None  # The tracking number can be updated if needed
    total_price: Optional[float] = None

    class Config:
        orm_mode = True

# Order schema with additional fields for retrieving an order (e.g., id, order_date)
class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: Optional[List[OrderDetail]] = None  # If applicable, add OrderDetail information

    class Config:
        orm_mode = True
