from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WarehouseBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: bool = True

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True