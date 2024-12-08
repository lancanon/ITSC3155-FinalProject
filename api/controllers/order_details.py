from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status, Response
from ..models import order_details as order_model, menu_items as menu_model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    # validate menu item exists
    menu_item = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == request.menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu item not found")

    # validate quantity
    if request.quantity <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="quantity must be greater than zero")

    # calculate the price for the order detail
    calculated_price = menu_item.price * request.quantity

    # create the new order detail
    new_item = order_model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        quantity=request.quantity,
        price=calculated_price
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
        # fetch all order details with joined menu items for optimization
        result = db.query(order_model.OrderDetail).options(
            joinedload(order_model.OrderDetail.menu_item)
        ).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        # fetch single order detail with related menu item
        item = db.query(order_model.OrderDetail).options(
            joinedload(order_model.OrderDetail.menu_item)
        ).filter(order_model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        # validate order detail exists
        item = db.query(order_model.OrderDetail).filter(order_model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")

        # validate quantity if provided
        if request.quantity is not None and request.quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="quantity must be greater than zero")

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
        # validate order detail exists
        item = db.query(order_model.OrderDetail).filter(order_model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")

        # delete the order detail
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
