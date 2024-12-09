from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, EmailStr, validator
from .order_details import OrderDetail

# Enum for payment methods
class PaymentMethod(str, Enum):
    credit_card = "Credit Card"
    paypal = "PayPal"
    cash = "Cash"
    apple_pay = "Apple Pay"

# Enum for payment statuses
class PaymentStatus(str, Enum):
    pending = "Pending"
    paid = "Paid"
    failed = "Failed"

# Represents an individual item in the order
class OrderItemCreate(BaseModel):
    menu_item_id: int  # ID of the menu item being ordered
    quantity: int  # Quantity of the menu item

    # Ensure the quantity is greater than zero
    @validator("quantity")
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than zero")
        return value

    class Config:
        orm_mode = True

# Base schema for orders (shared attributes between create, update, and read operations)
class OrderBase(BaseModel):
    customer_name: str  # Name of the customer placing the order
    description: Optional[str] = None  # Optional description for the order
    tracking_number: str  # Unique tracking number for the order
    total_price: float  # Total price of the order, including taxes
    order_type: str  # Type of order: "Takeout" or "Delivery"
    promotion_code: Optional[str] = None  # Promotion code applied to the order, if any
    payment_status: PaymentStatus = PaymentStatus.pending  # Default payment status

    # Ensure the total price is non-negative
    @validator("total_price")
    def validate_total_price(cls, value):
        if value < 0:
            raise ValueError("Total price must be non-negative")
        return value

    # Ensure the order type is either "Takeout" or "Delivery"
    @validator("order_type")
    def validate_order_type(cls, value):
        if value not in ["Takeout", "Delivery"]:
            raise ValueError("Order type must be 'Takeout' or 'Delivery'")
        return value

    class Config:
        orm_mode = True

# Schema for creating a new order
class OrderCreate(BaseModel):
    customer_name: str  # Name of the customer
    email: EmailStr  # Email to identify the customer
    phone_number: Optional[str] = None  # Optional phone number
    address: Optional[str] = None  # Required for "Delivery" orders
    menu_items: List[OrderItemCreate]  # List of menu items being ordered
    order_type: str = "Takeout"  # Default order type

    # Validate that address is required for delivery orders
    @validator("address", always=True)
    def validate_address_for_delivery(cls, value, values):
        if values.get("order_type") == "Delivery" and not value:
            raise ValueError("Address is required for delivery orders.")
        return value

    class Config:
        orm_mode = True

# Schema for updating an existing order
class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None  # Name of the customer
    description: Optional[str] = None  # Optional description
    tracking_number: Optional[str] = None  # Optional tracking number
    total_price: Optional[float] = None  # Optional total price
    order_type: Optional[str] = None  # Optional order type: "Takeout" or "Delivery"
    promotion_code: Optional[str] = None  # Optional promotion code
    payment_status: Optional[PaymentStatus] = None  # Optional payment status

    # Ensure the payment status is valid if provided
    @validator("payment_status", pre=True, always=True)
    def validate_payment_status(cls, value):
        if value and value not in PaymentStatus.__members__:
            raise ValueError("Invalid payment status")
        return value

    class Config:
        orm_mode = True

# Schema for processing a payment
class PaymentRequest(BaseModel):
    payment_method: PaymentMethod  # Payment method
    promo_code: Optional[str] = None  # Optional promo code

# Schema for retrieving an order (read operation)
class Order(OrderBase):
    id: int  # Unique identifier for the order
    order_date: Optional[datetime] = None  # Date when the order was placed
    order_details: Optional[List[OrderDetail]] = None  # Details of the order

    class Config:
        orm_mode = True

class TrackingResponse(BaseModel):
    tracking_number: str  # The order's tracking number
    status: str  # The order's current status

    class Config:
        orm_mode = True

# Schema for payment information response
class PaymentInformationResponse(BaseModel):
    message: str
    order_id: int
    final_price: float
    payment_status: str
    payment_type: str
    created_at: datetime 

    class Config:
        from_attributes = True