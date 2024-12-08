from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, List
from datetime import datetime, date
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..schemas.orders import OrderUpdate, PaymentRequest
from ..dependencies.database import get_db

router = APIRouter(
    tags=["orders"],
    prefix="/orders"
)

# Create a new order
@router.post("/", response_model=schema.Order)
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order with the provided details.
    """
    return controller.create_order(db=db, request=request)

# Fetch all orders with optional filters
@router.get("/", response_model=list[schema.Order])
def get_orders(
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    start_date: Optional[datetime] = Query(None, description="Start date for filtering orders"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering orders"),
    db: Session = Depends(get_db)
):
    """
    Fetch all orders with optional filters for:
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


# Update orders within a specific date range
@router.put("/{order_id}", response_model=schema.Order)
def update_order(
    order_id: int,
    updates: schema.OrderUpdate,  # Schema for fields that can be updated
    db: Session = Depends(get_db)
):
    """
    Update an order by its ID.
    """
    if not any(updates.dict(exclude_none=True).values()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No updates provided")
    return controller.update_order(db, order_id=order_id, updates=updates.dict(exclude_none=True))


# Delete orders within a specific date range
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order by its ID.
    """
    return controller.delete_order(db, order_id=order_id)


# Track the status of an order by its tracking number
@router.get("/track/{tracking_number}")
def track_order_status_route(tracking_number: str, db: Session = Depends(get_db)):
    """
    Track the status of an order using its tracking number.
    """
    return controller.track_order_status(db=db, tracking_number=tracking_number)

# Process payment for an order, including optional promo code
@router.post("/{order_id}/pay")
def pay_order(
    order_id: int,
    payment_request: PaymentRequest,
    db: Session = Depends(get_db)
):
    """
    Process payment for an order.
    """
    return controller.pay_order(
        db=db,
        order_id=order_id,
        payment_method=payment_request.payment_method.value,  # Extract string value from the Enum
        promo_code=payment_request.promo_code
    )

@router.get("/payment-methods", response_model=List[str])
def get_payment_methods():
    """
    Returns a list of supported payment methods.
    """
    return ["Credit Card", "PayPal", "Cash", "Apple Pay"]

@router.get("/daily-revenue")
def get_daily_revenue(
    revenue_date: date = Query(..., description="The date to calculate revenue for (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get the total revenue generated from food sales on a specific date.
    """
    # Ensure revenue_date is a date object
    return controller.calculate_daily_revenue(db=db, revenue_date=revenue_date)
