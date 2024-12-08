from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import customers as controller
from ..schemas import customers as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['customers'],
    prefix="/customers"
)

# create a new customer
@router.post("/", response_model=schema.Customer)
def create(request: schema.CustomerCreate, db: Session = Depends(get_db)):
    """
    create a new customer.
    """
    return controller.create(db=db, request=request)

# retrieve all customers with optional filters
@router.get("/", response_model=list[schema.Customer])
def read_all(email: str = None, phone_number: str = None, db: Session = Depends(get_db)):
    """
    retrieve all customers with optional filters for email or phone number.
    """
    customers = controller.read_all(db=db)
    if email:
        customers = [c for c in customers if c.email == email]
    if phone_number:
        customers = [c for c in customers if c.phone_number == phone_number]
    return customers

# retrieve a specific customer by id
@router.get("/{item_id}", response_model=schema.Customer)
def read_one(item_id: int, db: Session = Depends(get_db)):
    """
    retrieve a customer by id.
    """
    return controller.read_one(db, item_id=item_id)

# update a specific customer
@router.put("/{item_id}", response_model=schema.Customer)
def update(item_id: int, request: schema.CustomerUpdate, db: Session = Depends(get_db)):
    """
    update a customer by id.
    """
    return controller.update(db=db, request=request, item_id=item_id)

# delete a specific customer
@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    """
    delete a customer by id.
    """
    return controller.delete(db=db, item_id=item_id)
