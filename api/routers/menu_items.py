from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..controllers import menu_items as controller
from ..schemas import menu_items as schema
from ..dependencies.database import get_db
from ..schemas.menu_items import DietaryCategory

# Initialize the router for menu items
router = APIRouter(
    tags=["menu_items"],  # Tag for organizing the menu items endpoints in the API docs
    prefix="/menu_items"  # Base URL for all menu items routes
)

# Create a new menu item
@router.post("/", response_model=schema.MenuItem)
def create(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new menu item with ingredients from ResourceManagement.
    """
    return controller.create(db=db, request=request)


# Get all menu items with optional filters
@router.get("/", response_model=List[schema.MenuItem])
def read_all(
    category: Optional[DietaryCategory] = Query(None, description="Filter by dietary category"),
    available: Optional[bool] = Query(None, description="Filter by availability"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to fetch all menu items, optionally filtering by category and availability.
    """
    return controller.read_all(db=db, category=category, available=available)

# Get a specific menu item by ID
@router.get("/{item_id}", response_model=schema.MenuItem)
def read_one(item_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to fetch a single menu item by its ID.
    """
    return controller.read_one(db, item_id=item_id)

# Update a specific menu item by ID
@router.put("/{item_id}", response_model=schema.MenuItem)
def update(item_id: int, request: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing menu item by its ID.
    """
    return controller.update(db=db, request=request, item_id=item_id)

# Delete a specific menu item by ID
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(item_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a menu item by its ID.
    """
    return controller.delete(db=db, item_id=item_id)
