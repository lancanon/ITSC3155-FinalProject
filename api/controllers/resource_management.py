from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import resource_management as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_item = model.ResourceManagement(
        ingredient_name=request.ingredient_name,
        current_amount=request.current_amount,
        unit=request.unit,
        threshold_level=request.threshold_level
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item

def read_all(db: Session):
    try:
        return db.query(model.ResourceManagement).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.ResourceManagement).filter(model.ResourceManagement.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.ResourceManagement).filter(model.ResourceManagement.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
        for key, value in request.dict(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def delete(db: Session, item_id: int):
    try:
        item = db.query(model.ResourceManagement).filter(model.ResourceManagement.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
        db.delete(item)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
