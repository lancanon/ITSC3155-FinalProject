from fastapi import Response
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import orders as order_model
from ..models import customers as customer_model
from ..models import menu_items as menu_model
from ..models import order_details as order_detail_model
from sqlalchemy.exc import SQLAlchemyError
import uuid


def generate_tracking_number():
    #Generate a unique tracking number
    return str(uuid.uuid4())  

def create_order(db: Session, request):
    # Check if a customer with the provided email already exists
    customer = db.query(customer_model.Customer).filter(customer_model.Customer.email == request.email).first()

    if not customer:
        # If the customer doesn't exist, create a new customer for guest orders
        customer = customer_model.Customer(
            name=request.customer_name,
            email=request.email,
            phone_number=request.phone_number,
            address=request.address,
            password="guest_password",  # Default password for guest users
            saved_payment=None  # No saved payment info for guests
        )
        try:
            db.add(customer)
            db.commit()
            db.refresh(customer)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    # Generate a unique tracking number
    tracking_number = generate_tracking_number()

    # Create the order and link it to the customer (existing or newly created)
    new_order = order_model.Order(
        customer_id=customer.id,  # Link the order to the customer
        customer_name=request.customer_name,
        tracking_number=tracking_number,  # Automatically generated
        total_price=0  # Start with a total price of 0, which will be updated later
    )

    try:
        # First, add the order so that we can get the `id` for the order details
        db.add(new_order)
        db.commit()  # Commit to generate the `id`
        db.refresh(new_order)  # Refresh to get the order ID
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    # Initialize the total price
    total_price = 0

    # Add order details based on the menu items selected
    for item in request.menu_items:
        menu_item = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu item with ID {item.menu_item_id} not found")

        # Calculate the price for this order detail
        item_price = menu_item.price * item.quantity
        total_price += item_price

        # Create an order detail record (fixed import here)
        order_detail = order_detail_model.OrderDetail(
            order_id=new_order.id,  # Link the order detail to the created order
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
            price=item_price
        )
        db.add(order_detail)

    # Apply sales tax to total price (for example, 7%)
    total_price += total_price * 0.07
    new_order.total_price = total_price

    try:
        # Final commit to save the updated order and order details
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order



def read_all(db: Session):
    try:
        result = db.query(order_model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete(db: Session, item_id):
    try:
        item = db.query(order_model.Order).filter(order_model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
