from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas.promotions import PromotionCreate, PromotionUpdate, PromotionResponse
from ..controllers.promotions import (
    create_promotion,
    read_all_promotions,
    read_promotion,
    update_promotion,
    delete_promotion
)
from typing import List, Optional

router = APIRouter(
    tags=["Promotions"],
    prefix="/promotions"
)

# Create a promotion
@router.post("/", response_model=PromotionResponse, status_code=status.HTTP_201_CREATED)
def create(request: PromotionCreate, db: Session = Depends(get_db)):
    return create_promotion(db, request)

# Get all promotions
@router.get("/", response_model=List[PromotionResponse])
def read_all(active_only: Optional[bool] = False, db: Session = Depends(get_db)):
    return read_all_promotions(db, active_only)

# Get a promotion by ID
@router.get("/{promotion_id}", response_model=PromotionResponse)
def read(promotion_id: int, db: Session = Depends(get_db)):
    return read_promotion(db, promotion_id)

# Update a promotion
@router.put("/{promotion_id}", response_model=PromotionResponse)
def update(promotion_id: int, request: PromotionUpdate, db: Session = Depends(get_db)):
    return update_promotion(db, promotion_id, request)

# Delete a promotion
@router.delete("/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(promotion_id: int, db: Session = Depends(get_db)):
    return delete_promotion(db, promotion_id)
