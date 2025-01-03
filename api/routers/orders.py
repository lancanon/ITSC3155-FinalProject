from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..schemas.orders import (
    OrderCreate,
    OrderUpdate,
    PaymentRequest,
    TrackingResponse,
    PaymentInformationResponse,  # Add this import
    Order,
)

from ..dependencies.database import get_db

router = APIRouter(
    tags=["orders"],
    prefix="/orders"
)

# Create a new order
@router.post("/", response_model=schema.Order, status_code=status.HTTP_201_CREATED)
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order with the provided details.
    """
    return controller.create_order(db=db, request=request)

# Fetch all orders with optional filters
@router.get("/", response_model=List[schema.Order])
def get_orders(
    status: Optional[str] = Query(None, description="Filter orders by status"),
    customer_id: Optional[int] = Query(None, description="Filter orders by customer ID"),
    start_date: Optional[datetime] = Query(None, description="Start date for filtering orders (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering orders (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Fetch all orders with optional filters:
    - Status
    - Customer ID
    - Date Range (start_date and end_date)
    """
    return controller.read_all(
        db=db,
        status=status,
        customer_id=customer_id,
        start_date=start_date,
        end_date=end_date
    )

# Update an order by ID
@router.put("/{order_id}", response_model=schema.Order)
def update_order(
    order_id: int,
    updates: schema.OrderUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an order by its ID.
    Fields to update are provided in the request body.
    """
    if not updates.dict(exclude_unset=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update provided")
    return controller.update_order(db, order_id=order_id, updates=updates.dict(exclude_unset=True))

# Delete an order by ID
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order by its ID.
    """
    return controller.delete_order(db, order_id=order_id)

# Track the status of an order by its tracking number
@router.get("/track/{tracking_number}", response_model=schema.TrackingResponse)
def track_order_status(tracking_number: str, db: Session = Depends(get_db)):
    """
    Track the status of an order using its tracking number.
    """
    return controller.track_order_status(db=db, tracking_number=tracking_number)


# Process payment for an order
@router.post("/{order_id}/pay", response_model=schema.PaymentInformationResponse)
def pay_order(
    order_id: int,
    payment_request: schema.PaymentRequest,
    db: Session = Depends(get_db)
):
    """
    Process payment for an order.
    """
    return controller.pay_order(
        db=db,
        order_id=order_id,
        payment_method=payment_request.payment_method,
        promo_code=payment_request.promo_code
    )

# Get a list of supported payment methods
@router.get("/payment-methods", response_model=List[str])
def get_payment_methods():
    """
    Returns a list of supported payment methods.
    """
    return ["Credit Card", "PayPal", "Cash", "Apple Pay"]

# Get the total revenue for a specific date
@router.get("/daily-revenue", response_model=dict)
def get_daily_revenue(
    revenue_date: date = Query(..., description="The date to calculate revenue for (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get the total revenue generated from food sales on a specific date.
    """
    return controller.calculate_daily_revenue(db=db, revenue_date=revenue_date)
