from fastapi import APIRouter, Depends, status 
from sqlalchemy.orm import Session
from ..controllers import resource_management as controller
from ..schemas import resource_management as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["resources"],
    prefix="/resource"
)

@router.post("/", response_model=schema.ResourceManagement, status_code=status.HTTP_201_CREATED)
def create(request: schema.ResourceManagementCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.ResourceManagement])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.ResourceManagement)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.ResourceManagement)
def update(item_id: int, request: schema.ResourceManagementUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
