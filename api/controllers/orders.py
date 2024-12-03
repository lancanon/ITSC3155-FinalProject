from fastapi import Response
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import orders as order_model
from ..models import customers as customer_model
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
            password="guest_password",  
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

    # Check if tracking number already exists in the database (optional but adds safety)
    existing_order = db.query(order_model.Order).filter(order_model.Order.tracking_number == tracking_number).first()
    if existing_order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tracking number already exists.")
    
    # Create the order and link it to the customer (existing or newly created)
    new_item = order_model.Order(
        customer_id=customer.id,  # Link the order to the customer
        customer_name=request.customer_name,
        description=request.description,
        tracking_number=tracking_number,  # Automatically generated
        total_price=request.total_price
    )
    
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return new_item




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
