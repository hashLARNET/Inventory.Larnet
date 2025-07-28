from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    barcode: str
    stock: int = 0
    unit_price: Optional[Decimal] = None
    obra: str
    n_factura: str
    warehouse_id: uuid.UUID

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    unit_price: Optional[Decimal] = None
    obra: Optional[str] = None
    n_factura: Optional[str] = None

class Item(ItemBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True