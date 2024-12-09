from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional
from fastapi import HTTPException, status, Response
from ..models import orders as order_model, customers as customer_model, menu_items as menu_model, order_details as order_detail_model, resource_management as resource_model
from ..models.orders import Order
from ..models.payment_info import PaymentInformation
from ..models.promotions import Promotion
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
import uuid


# Utility to generate a unique tracking number
def generate_tracking_number():
    return str(uuid.uuid4())


# Create a new order with inventory checks
def create_order(db: Session, request):
    # Validate menu items in the order
    if not request.menu_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must include at least one menu item"
        )

    # Fetch or create customer
    customer = db.query(customer_model.Customer).filter(
        (customer_model.Customer.email == request.email) |
        (customer_model.Customer.phone_number == request.phone_number)
    ).first()

    if not customer:
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

    # Create order
    tracking_number = generate_tracking_number()
    new_order = order_model.Order(
        customer_id=customer.id,
        customer_name=customer.name,
        tracking_number=tracking_number,
        total_price=0,
        status="Pending",
        order_type=request.order_type
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Process menu items
    total_price = 0
    for item in request.menu_items:
        menu_item = db.query(menu_model.MenuItem).filter(
            menu_model.MenuItem.id == item.menu_item_id
        ).first()

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with ID {item.menu_item_id} not found"
            )

        # Deduct inventory and calculate price
        for resource in menu_item.resources:
            required_quantity = resource.threshold_level * item.quantity
            if resource.current_amount < required_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough {resource.ingredient_name}. Required: {required_quantity}, Available: {resource.current_amount}"
                )
            resource.current_amount -= required_quantity
            db.commit()

        # Add order details
        item_price = menu_item.price * item.quantity
        total_price += item_price
        order_detail = order_detail_model.OrderDetail(
            order_id=new_order.id,
            menu_item_id=menu_item.id,
            quantity=item.quantity,
            price=item_price
        )
        db.add(order_detail)

    # Finalize order
    new_order.total_price = total_price * 1.07  # Add 7% sales tax
    db.commit()
    db.refresh(new_order)

    return new_order

    # Validate menu items in the order
    if not request.menu_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must include at least one menu item"
        )

    # Fetch or create customer
    customer = db.query(customer_model.Customer).filter(
        (customer_model.Customer.email == request.email) |
        (customer_model.Customer.phone_number == request.phone_number)
    ).first()

    if not customer:
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

    # Create order
    tracking_number = generate_tracking_number()
    new_order = order_model.Order(
        customer_id=customer.id,
        customer_name=customer.name,
        tracking_number=tracking_number,
        total_price=0,
        status="Pending",
        order_type=request.order_type
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Process menu items
    total_price = 0
    for item in request.menu_items:
        # Access attributes of the OrderItemCreate model
        menu_item = db.query(menu_model.MenuItem).filter(
            menu_model.MenuItem.id == item.menu_item_id
        ).first()

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with ID {item.menu_item_id} not found"
            )

        # Check inventory for required ingredients
        for resource in menu_item.resources:
            required_quantity = resource.threshold_level * item.quantity
            if resource.current_amount < required_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough {resource.ingredient_name}. Required: {required_quantity}, Available: {resource.current_amount}"
                )

        # Calculate price and add to order details
        item_price = menu_item.price * item.quantity
        total_price += item_price
        order_detail = order_detail_model.OrderDetail(
            order_id=new_order.id,
            menu_item_id=menu_item.id,
            quantity=item.quantity,
            price=item_price
        )
        db.add(order_detail)

    # Deduct inventory
    for item in request.menu_items:
        menu_item = db.query(menu_model.MenuItem).filter(
            menu_model.MenuItem.id == item.menu_item_id
        ).first()

        for resource in menu_item.resources:
            required_quantity = resource.threshold_level * item.quantity
            resource.current_amount -= required_quantity
            db.commit()

    # Finalize order
    new_order.total_price = total_price * 1.07  # Add 7% sales tax
    db.commit()
    db.refresh(new_order)

    return new_order
    # Validate menu items in the order
    if not request.menu_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must include at least one menu item"
        )

    # Fetch or create customer
    customer = db.query(customer_model.Customer).filter(
        (customer_model.Customer.email == request.email) |
        (customer_model.Customer.phone_number == request.phone_number)
    ).first()

    if not customer:
        customer = customer_model.Customer(
            name=request.customer_name,
            email=request.email,
            phone_number=request.phone_number,
            address=request.address,
            password="guest_password"  # Placeholder
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

    # Create order
    tracking_number = generate_tracking_number()
    new_order = order_model.Order(
        customer_id=customer.id,
        customer_name=customer.name,
        tracking_number=tracking_number,
        total_price=0,
        status="Pending",
        order_type=request.order_type
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Process menu items
    total_price = 0
    for item in request.menu_items:
        menu_item = db.query(menu_model.MenuItem).filter(
            menu_model.MenuItem.id == item["menu_item_id"]
        ).first()

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with ID {item['menu_item_id']} not found"
            )

        # Check inventory for required ingredients
        for resource in menu_item.resources:
            required_quantity = resource.threshold_level * item["quantity"]
            if resource.current_amount < required_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough {resource.ingredient_name}. Required: {required_quantity}, Available: {resource.current_amount}"
                )

        # Calculate price and add to order details
        item_price = menu_item.price * item["quantity"]
        total_price += item_price
        order_detail = order_detail_model.OrderDetail(
            order_id=new_order.id,
            menu_item_id=menu_item.id,
            quantity=item["quantity"],
            price=item_price
        )
        db.add(order_detail)

    # Deduct inventory
    for item in request.menu_items:
        menu_item = db.query(menu_model.MenuItem).filter(
            menu_model.MenuItem.id == item["menu_item_id"]
        ).first()

        for resource in menu_item.resources:
            required_quantity = resource.threshold_level * item["quantity"]
            resource.current_amount -= required_quantity
            db.commit()

    # Finalize order
    new_order.total_price = total_price * 1.07  # Add 7% sales tax
    db.commit()
    db.refresh(new_order)

    return new_order


# Retrieve all orders with optional filters
def read_all(db: Session, status: Optional[str] = None, customer_id: Optional[int] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    try:
        query = db.query(Order)
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving orders: {str(e)}"
        )


# Update an order
def update_order(db: Session, order_id: int, updates: dict):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in updates.items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order


# Delete an order
def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": f"Order {order_id} deleted successfully"}


# Track order status
def track_order_status(db: Session, tracking_number: str):
    order = db.query(Order).filter(Order.tracking_number == tracking_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"tracking_number": order.tracking_number, "status": order.status}


# Pay for an order
def pay_order(db: Session, order_id: int, payment_method: str, promo_code: Optional[str] = None):
    # Fetch the order by ID
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

    # Store the original price
    if not order.original_price:
        order.original_price = order.total_price

    # Calculate final price
    final_price = max(0, order.total_price - discount)

    # Update payment status and total price
    order.payment_status = "Paid"
    order.total_price = final_price
    db.commit()
    db.refresh(order)

    # Create a payment information record
    payment_info = PaymentInformation(
        order_id=order.id,
        payment_type=payment_method,
        transaction_status="Completed",
    )
    db.add(payment_info)
    db.commit()
    db.refresh(payment_info)

    return {
        "message": "Payment processed successfully",
        "order_id": order.id,
        "final_price": final_price,
        "payment_status": payment_info.transaction_status,
        "payment_type": payment_info.payment_type,
        "created_at": payment_info.created_at,
    }


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

    # Create a payment info record
    payment_info = PaymentInformation(
        order_id=order_id,
        payment_type=payment_method,
        transaction_status="Completed"
    )
    db.add(payment_info)
    db.commit()

    return payment_info


# Calculate daily revenue
def calculate_daily_revenue(db: Session, revenue_date: date):
    total_revenue = db.query(func.sum(Order.original_price)).filter(
        func.date(Order.order_date) == revenue_date,
        Order.payment_status == "Paid"
    ).scalar() or 0
    return {"date": revenue_date, "total_revenue": total_revenue}
