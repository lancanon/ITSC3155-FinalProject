from fastapi import Response, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import promotions as promo_model
from ..schemas.promotions import PromotionCreate, PromotionUpdate


def create_promotion(db: Session, request: PromotionCreate):
    if request.discount_percentage <= 0 or request.discount_percentage > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Discount percentage must be between 0 and 100.")

    new_promo = promo_model.Promotion(
        code=request.code,
        description=request.description,
        discount_percentage=request.discount_percentage,
        expiration_date=request.expiration_date,
        is_active=request.is_active
    )
    try:
        db.add(new_promo)
        db.commit()
        db.refresh(new_promo)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return new_promo


def update_promotion(db: Session, promo_id: int, request: PromotionUpdate):
    promo = db.query(promo_model.Promotion).filter(promo_model.Promotion.id == promo_id).first()
    if not promo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found!")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(promo, key, value)

    try:
        db.commit()
        db.refresh(promo)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return promo
