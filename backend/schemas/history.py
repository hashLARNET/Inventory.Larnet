from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class HistoryBase(BaseModel):
    action_type: str
    item_name: str
    quantity: int
    obra: str
    n_factura: str
    warehouse_name: str
    user_name: str
    notes: Optional[str] = None

class History(HistoryBase):
    id: uuid.UUID
    action_date: datetime
    
    class Config:
        from_attributes = True