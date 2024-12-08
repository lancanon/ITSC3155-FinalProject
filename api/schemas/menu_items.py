from pydantic import BaseModel, validator
from enum import Enum
from typing import Optional, Dict


# Define dietary categories as an Enum
class DietaryCategory(str, Enum):
    vegetarian = "Vegetarian"
    non_vegetarian = "Non-Vegetarian"
    pescatarian = "Pescatarian"
    vegan = "Vegan"


# Base schema for menu item
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: Optional[Dict[str, float]] = None  # Ingredients as a structured dictionary
    price: float
    calories: Optional[int] = None
    menu_category: str
    dietary_category: Optional[DietaryCategory] = None
    available: bool = True

    # Validators for `price` and `calories`
    @validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be greater than zero")
        return value

    @validator("calories")
    def validate_calories(cls, value):
        if value is not None and value < 0:
            raise ValueError("Calories cannot be negative")
        return value

    @validator("ingredients")
    def validate_ingredients(cls, value):
        if value is not None:
            if not isinstance(value, dict):
                raise ValueError("Ingredients must be a dictionary of {ingredient_name: quantity}")
            if not all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in value.items()):
                raise ValueError("All keys must be strings and all values must be numeric (int or float).")
        return value


# Schema for creating a new menu item
class MenuItemCreate(MenuItemBase):
    ingredients: Dict[str, float]  # Ensure ingredients are required when creating


# Schema for updating an existing menu item
class MenuItemUpdate(BaseModel):
    description: Optional[str] = None
    ingredients: Optional[Dict[str, float]] = None  # Structured data for updates
    price: Optional[float] = None
    calories: Optional[int] = None
    menu_category: Optional[str] = None
    dietary_category: Optional[DietaryCategory] = None
    available: Optional[bool] = None

    @validator("price")
    def validate_update_price(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Price must be greater than zero")
        return value

    @validator("calories")
    def validate_update_calories(cls, value):
        if value is not None and value < 0:
            raise ValueError("Calories cannot be negative")
        return value

    @validator("ingredients")
    def validate_update_ingredients(cls, value):
        if value is not None:
            if not isinstance(value, dict):
                raise ValueError("Ingredients must be a dictionary of {ingredient_name: quantity}")
            if not all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in value.items()):
                raise ValueError("All keys must be strings and all values must be numeric (int or float).")
        return value


# Schema for returning menu item data
class MenuItem(MenuItemBase):
    id: int

    class Config:
        from_attributes = True
