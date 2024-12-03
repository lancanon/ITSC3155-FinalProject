from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)

# Route for creating an order with an existing customer account
@router.post("/", response_model=schema.Order)
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create_order(db=db, request=request)


# Route to fetch all orders
@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

# Route to fetch a single order by its ID
@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

# Route to update an existing order
@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

# Route to delete an order
@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
