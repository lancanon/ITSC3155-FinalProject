from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: Optional[str] = None
    price: float
    calories: Optional[int] = None
    menu_category: str
    dietary_category: Optional[str] = None
    available: bool = True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    description: Optional[str] = None
    ingredients: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    menu_category: Optional[str] = None
    dietary_category: Optional[str] = None
    available: Optional[bool] = None

class MenuItem(MenuItemBase):
    id: int

    class Config:
        orm_mode = True
