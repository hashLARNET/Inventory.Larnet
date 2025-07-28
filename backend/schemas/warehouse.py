from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class WarehouseBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: bool = True

class WarehouseCreate(WarehouseBase):
    pass

class Warehouse(WarehouseBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True