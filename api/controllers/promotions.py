from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.promotions import Promotion
from ..schemas.promotions import PromotionCreate, PromotionUpdate
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

# Create a promotion
def create_promotion(db: Session, request: PromotionCreate):
    new_promotion = Promotion(
        code=request.code,
        description=request.description,
        discount_percentage=request.discount_percentage,
        expiration_date=request.expiration_date,
        is_active=request.is_active
    )

    try:
        db.add(new_promotion)
        db.commit()
        db.refresh(new_promotion)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_promotion

# Get all promotions
def read_all_promotions(db: Session, active_only: bool = False):
    query = db.query(Promotion)
    if active_only:
        query = query.filter(Promotion.is_active == True, Promotion.expiration_date >= date.today())
    return query.all()

# Get a promotion by ID
def read_promotion(db: Session, promotion_id: int):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    return promotion

# Update a promotion
def update_promotion(db: Session, promotion_id: int, request: PromotionUpdate):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    
    for key, value in request.dict(exclude_unset=True).items():
        setattr(promotion, key, value)

    db.commit()
    db.refresh(promotion)
    return promotion

# Delete a promotion
def delete_promotion(db: Session, promotion_id: int):
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    
    db.delete(promotion)
    db.commit()
    return {"message": "Promotion deleted successfully"}
