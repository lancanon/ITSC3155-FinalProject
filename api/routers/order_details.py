from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import order_details as controller
from ..schemas import order_details as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['order details'],
    prefix="/orderdetails"
)

# create a new order detail
@router.post("/", response_model=schema.OrderDetail)
def create(request: schema.OrderDetailCreate, db: Session = Depends(get_db)):
    """
    create a new order detail.
    """
    return controller.create(db=db, request=request)

# retrieve all order details with optional filters
@router.get("/", response_model=list[schema.OrderDetail])
def read_all(order_id: int = None, db: Session = Depends(get_db)):
    """
    fetch all order details with optional filter by order_id.
    """
    result = controller.read_all(db=db)
    if order_id:
        result = [detail for detail in result if detail.order_id == order_id]
    return result

# retrieve a specific order detail by id
@router.get("/{item_id}", response_model=schema.OrderDetail)
def read_one(item_id: int, db: Session = Depends(get_db)):
    """
    fetch a specific order detail by id.
    """
    return controller.read_one(db, item_id=item_id)

# update an existing order detail
@router.put("/{item_id}", response_model=schema.OrderDetail)
def update(item_id: int, request: schema.OrderDetailUpdate, db: Session = Depends(get_db)):
    """
    update an order detail by id.
    """
    return controller.update(db=db, request=request, item_id=item_id)

# delete an existing order detail
@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    """
    delete an order detail by id.
    """
    return controller.delete(db=db, item_id=item_id)
