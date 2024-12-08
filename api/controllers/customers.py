from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import customers as model
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext

# set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create(db: Session, request):
    # validate email uniqueness
    if db.query(model.Customer).filter(model.Customer.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists")
    
    # validate phone number uniqueness
    if db.query(model.Customer).filter(model.Customer.phone_number == request.phone_number).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="phone number already exists")
    
    # hash the password before saving
    hashed_password = pwd_context.hash(request.password)
    
    # create a new customer
    new_item = model.Customer(
        name=request.name,
        phone_number=request.phone_number,
        email=request.email,
        address=request.address,
        password=hashed_password
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
        result = db.query(model.Customer).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Customer).filter(model.Customer.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="customer not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        # fetch customer by id
        item = db.query(model.Customer).filter(model.Customer.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="customer not found")
        
        # ensure email and phone number uniqueness if provided
        if request.email and db.query(model.Customer).filter(model.Customer.email == request.email).filter(model.Customer.id != item_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists")
        if request.phone_number and db.query(model.Customer).filter(model.Customer.phone_number == request.phone_number).filter(model.Customer.id != item_id).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="phone number already exists")

        # apply updates
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Customer).filter(model.Customer.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="customer not found")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
