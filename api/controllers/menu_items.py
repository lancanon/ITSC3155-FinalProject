from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status, Response
from ..models import menu_items as model, resource_management as resource_model
from ..models.menu_items import MenuItem
from ..models.resource_management import ResourceManagement  # Import the ResourceManagement model
from ..models.menu_item_ingredients import menu_item_ingredients  # Import the association table
from typing import Optional
from ..schemas.menu_items import DietaryCategory
from sqlalchemy.exc import SQLAlchemyError
import json


# Utility to validate ingredients against ResourceManagement
def validate_ingredients(db: Session, ingredients: dict):
    for ingredient_name, quantity in ingredients.items():
        resource = db.query(resource_model.ResourceManagement).filter(
            resource_model.ResourceManagement.ingredient_name == ingredient_name
        ).first()
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingredient '{ingredient_name}' not found in resource management"
            )
        if quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid quantity for ingredient '{ingredient_name}'"
            )
    return ingredients


# Create a new menu item
def create(db: Session, request):
    new_item = MenuItem(
        name=request.name,
        description=request.description,
        price=request.price,
        calories=request.calories,
        menu_category=request.menu_category,
        dietary_category=request.dietary_category,
        available=request.available
    )

    try:
        # Link ingredients
        for ingredient_name, quantity in request.ingredients.items():
            resource = db.query(ResourceManagement).filter(
                ResourceManagement.ingredient_name == ingredient_name
            ).first()
            if not resource:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient '{ingredient_name}' not found"
                )
            # Add the resource to the menu item's resources
            new_item.resources.append(resource)

        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


# Get all menu items with optional filters
# Example: Accessing resources in read_all
def read_all(db: Session, category: Optional[str] = None, available: Optional[bool] = None):
    try:
        # Build the query
        query = db.query(MenuItem)
        
        if category:
            query = query.filter(MenuItem.dietary_category == category)
        if available is not None:
            query = query.filter(MenuItem.available == available)

        # Fetch all menu items
        items = query.all()

        # Log related resources for debugging
        for item in items:
            print(f"Menu Item: {item.name}, Resources: {[resource.ingredient_name for resource in item.resources]}")
        
        return items
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

# Get a specific menu item by ID
def read_one(db: Session, item_id: int):
    """
    Fetch a single menu item by its ID, including its associated ingredients.
    """
    try:
        # Use `joinedload` to eagerly load the related resources
        item = db.query(MenuItem).options(joinedload(MenuItem.resources)).filter(MenuItem.id == item_id).first()
        
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

        # Extract resources (ingredients) into a dictionary
        ingredients = {
            resource.ingredient_name: resource.current_amount
            for resource in item.resources
        }

        # Include the parsed ingredients in the response
        result = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "calories": item.calories,
            "menu_category": item.menu_category,
            "dietary_category": item.dietary_category,
            "available": item.available,
            "ingredients": ingredients
        }

        return result
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database Error: {error}")

# Update a menu item by ID
def update(db: Session, item_id: int, request):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

    try:
        # Update general fields
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key != "ingredients":
                setattr(item, key, value)

        # Update ingredients
        if request.ingredients:
            item.resources.clear()  # Clear existing resources
            for ingredient_name, quantity in request.ingredients.items():
                resource = db.query(ResourceManagement).filter(
                    ResourceManagement.ingredient_name == ingredient_name
                ).first()
                if not resource:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Ingredient '{ingredient_name}' not found"
                    )
                item.resources.append(resource)

        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


# Delete a menu item by ID
def delete(db: Session, item_id: int):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
        db.delete(item)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
