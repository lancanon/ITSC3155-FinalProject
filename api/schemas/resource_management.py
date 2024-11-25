from pydantic import BaseModel, Optional

class ResourceManagementBase(BaseModel):
    ingredient_name: str
    current_amount: float
    unit: str
    threshold_level: float

class ResourceManagementCreate(ResourceManagementBase):
    pass

class ResourceManagementUpdate(BaseModel):
    current_amount: Optional[float] = None
    threshold_level: Optional[float] = None

class ResourceManagement(ResourceManagementBase):
    id: int

    class Config:
        orm_mode = True
