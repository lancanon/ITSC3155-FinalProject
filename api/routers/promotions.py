from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import promotions as promo_controller
from ..schemas.promotions import PromotionCreate, PromotionUpdate, Promotion
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Promotions'],
    prefix="/promotions"
)

@router.post("/", response_model=Promotion)
def create_promotion(request: PromotionCreate, db: Session = Depends(get_db)):
    return promo_controller.create_promotion(db=db, request=request)


@router.put("/{promo_id}", response_model=Promotion)
def update_promotion(promo_id: int, request: PromotionUpdate, db: Session = Depends(get_db)):
    return promo_controller.update_promotion(db=db, promo_id=promo_id, request=request)
