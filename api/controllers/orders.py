from fastapi import Response, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Optional 
from ..models import orders as order_model, customers as customer_model, menu_items as menu_model, order_details as order_detail_model, resource_management as resource_model
from ..models.orders import Order  
from ..models.promotions import Promotion
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
import uuid

# Utility to generate a unique tracking number
def generate_tracking_number():
    return str(uuid.uuid4())

# Create a new order with inventory check
def create_order(db: Session, request):
    # Validate that the order contains menu items
    if not request.menu_items or len(request.menu_items) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must include at least one menu item")

    # Check if the customer already exists by email or phone number
    customer = db.query(customer_model.Customer).filter(
        (customer_model.Customer.email == request.email) |
        (customer_model.Customer.phone_number == request.phone_number)
    ).first()

    if not customer:
        # Create a new guest customer if not found
        customer = customer_model.Customer(
            name=request.customer_name,
            email=request.email,
            phone_number=request.phone_number,
            address=request.address,
            password="guest_password"  # Placeholder password
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
    else:
        # Handle duplicate gracefully
        if customer.phone_number == request.phone_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer with phone number {request.phone_number} already exists."
            )

    # Generate a unique tracking number for the order
    tracking_number = generate_tracking_number()

    # Create the order linked to the customer
    new_order = order_model.Order(
        customer_id=customer.id,
        customer_name=request.customer_name,
        tracking_number=tracking_number,
        total_price=0  # Initial placeholder
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Check ingredient availability and calculate total price
    total_price = 0
    for item in request.menu_items:
        # Fetch the menu item details
        menu_item = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item with ID {item.menu_item_id} not found")

        # Validate ingredient availability
        for ingredient_name, required_quantity in menu_item.ingredients.items():  # Ingredients as a dictionary
            resource = db.query(resource_model.ResourceManagement).filter(
                resource_model.ResourceManagement.ingredient_name == ingredient_name
            ).first()
            if not resource:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient {ingredient_name} not found in inventory"
                )
            if resource.current_amount < required_quantity * item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient {ingredient_name}. Required: {required_quantity * item.quantity}, Available: {resource.current_amount}"
                )

        # Calculate price for the item
        item_price = menu_item.price * item.quantity
        total_price += item_price

        # Create order detail entry
        order_detail = order_detail_model.OrderDetail(
            order_id=new_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            price=item_price
        )
        db.add(order_detail)

    # Deduct ingredient quantities from inventory
    for item in request.menu_items:
        menu_item = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == item.menu_item_id).first()
        for ingredient_name, required_quantity in menu_item.ingredients.items():
            resource = db.query(resource_model.ResourceManagement).filter(
                resource_model.ResourceManagement.ingredient_name == ingredient_name
            ).first()
            if resource:
                resource.current_amount -= required_quantity * item.quantity
                db.commit()

    # Add sales tax and finalize total price
    total_price += total_price * 0.07  # Add 7% sales tax
    new_order.total_price = total_price
    db.commit()
    db.refresh(new_order)

    return new_order

    # Validate that the order contains menu items
    if not request.menu_items or len(request.menu_items) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must include at least one menu item")

    # Check if the customer already exists by email or phone number
    customer = db.query(customer_model.Customer).filter(
        (customer_model.Customer.email == request.email) |
        (customer_model.Customer.phone_number == request.phone_number)
    ).first()

    if not customer:
        # Create a new guest customer if not found
        customer = customer_model.Customer(
            name=request.customer_name,
            email=request.email,
            phone_number=request.phone_number,
            address=request.address,
            password="guest_password"  # Placeholder password
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
    else:
        # Handle duplicate gracefully
        if customer.phone_number == request.phone_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer with phone number {request.phone_number} already exists."
            )

    # Generate a unique tracking number for the order
    tracking_number = generate_tracking_number()

    # Create the order linked to the customer
    new_order = order_model.Order(
        customer_id=customer.id,
        customer_name=request.customer_name,
        tracking_number=tracking_number,
        total_price=0  # Initial placeholder
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Check ingredient availability and calculate total price
    total_price = 0
    for item in request.menu_items:
        # Fetch the menu item details
        menu_item = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item with ID {item.menu_item_id} not found")

        # Validate ingredient availability
        ingredient_list = menu_item.ingredients.split(",")  # Assuming ingredients are comma-separated
        for ingredient_name in ingredient_list:
            resource = db.query(resource_model.ResourceManagement).filter(
                resource_model.ResourceManagement.ingredient_name == ingredient_name.strip()
            ).first()
            if not resource:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient {ingredient_name.strip()} not found in inventory"
                )
            if resource.current_amount < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient {ingredient_name.strip()}. Required: {item.quantity}, Available: {resource.current_amount}"
                )

        # Calculate price for the item
        item_price = menu_item.price * item.quantity
        total_price += item_price

        # Create order detail entry
        order_detail = order_detail_model.OrderDetail(
            order_id=new_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            price=item_price
        )
        db.add(order_detail)

    # Deduct ingredient quantities from inventory
    for item in request.menu_items:
        menu_item = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == item.menu_item_id).first()
        ingredient_list = menu_item.ingredients.split(",")
        for ingredient_name in ingredient_list:
            resource = db.query(resource_model.ResourceManagement).filter(
                resource_model.ResourceManagement.ingredient_name == ingredient_name.strip()
            ).first()
            if resource:
                resource.current_amount -= item.quantity
                db.commit()

    # Add sales tax and finalize total price
    total_price += total_price * 0.07  # Add 7% sales tax
    new_order.total_price = total_price
    db.commit()
    db.refresh(new_order)

    return new_order


# Retrieve all orders with optional filters
def read_all(
    db: Session,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    try:
        query = db.query(Order)
        
        # Apply filters
        if status:
            query = query.filter(Order.status == status)
        if customer_id:
            query = query.filter(Order.customer_id == customer_id)
        if start_date:
            query = query.filter(Order.order_date >= start_date)
        if end_date:
            query = query.filter(Order.order_date <= end_date)
        
        return query.all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching orders: {str(e)}"
        )

def update_order(db: Session, order_id: int, updates: Dict[str, Optional[str]]):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in updates.items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": f"Order {order_id} deleted successfully"}


# Track the status of an order
def track_order_status(db: Session, tracking_number: str):
    try:
        # Query the order by tracking number
        order = db.query(order_model.Order).filter(order_model.Order.tracking_number == tracking_number).first()

        # If order not found, raise an HTTPException
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order with the given tracking number not found"
            )

        # Return the order's tracking number and status
        return {"tracking_number": order.tracking_number, "status": order.status}

    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the order: {str(e)}"
        )

def pay_order(db: Session, order_id: int, payment_method: str, promo_code: Optional[str] = None):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.payment_status == "Paid":
        raise HTTPException(status_code=400, detail="Order is already paid")

    # Validate and apply promo code
    discount = 0
    if promo_code:
        promotion = db.query(Promotion).filter(
            Promotion.code == promo_code,
            Promotion.is_active == True,
            Promotion.expiration_date >= datetime.utcnow()
        ).first()
        if not promotion:
            raise HTTPException(status_code=400, detail="Invalid or expired promo code")
        discount = promotion.discount_percentage / 100 * order.total_price

    # Update payment status and apply discount
    order.payment_status = "Paid"
    order.total_price -= discount  # Apply the discount
    db.commit()
    db.refresh(order)

    return order



def calculate_daily_revenue(db: Session, revenue_date: date):
    try:
        total_revenue = db.query(func.sum(Order.total_price)).filter(
            func.date(Order.order_date) == revenue_date  # Ensure the correct date comparison
        ).scalar()

        if total_revenue is None:
            total_revenue = 0  # No orders found for the given date

        return {"date": revenue_date, "total_revenue": total_revenue}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while calculating revenue: {str(e)}"
        )
