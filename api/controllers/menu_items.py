from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import menu_items as model, resource_management as resource_model
from ..models.menu_items import MenuItem
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
    new_item = model.MenuItem(
        name=request.name,
        description=request.description,
        price=request.price,
        calories=request.calories,
        menu_category=request.menu_category,
        dietary_category=request.dietary_category,
        available=request.available
    )

    # Add ingredients to the menu item
    for ingredient_id, amount in request.ingredients.items():
        resource = db.query(model.ResourceManagement).filter_by(id=ingredient_id).first()
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingredient with ID {ingredient_id} not found"
            )
        new_item.ingredients.append(resource)

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


# Get all menu items with optional filters
# Example: Accessing resources in read_all
def read_all(db: Session, category: Optional[DietaryCategory] = None, available: Optional[bool] = None):
    query = db.query(MenuItem)

    if category:
        query = query.filter(MenuItem.dietary_category == category.value)
    if available is not None:
        query = query.filter(MenuItem.available == available)

    try:
        items = query.all()
        for item in items:
            item.resources = [resource for resource in item.resources]  # Access related resources
        return items
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get a specific menu item by ID
def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

        item.ingredients = json.loads(item.ingredients)  # Parse JSON to dictionary
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


# Update a menu item by ID
def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.MenuItem).filter(model.MenuItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

        if request.ingredients:
            # Validate and link updated ingredients
            validated_ingredients = validate_ingredients(db, request.ingredients)
            item.ingredients = json.dumps(validated_ingredients)

        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key != "ingredients":
                setattr(item, key, value)

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
