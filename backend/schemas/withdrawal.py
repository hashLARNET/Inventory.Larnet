from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

class WithdrawalItemBase(BaseModel):
    item_id: uuid.UUID
    quantity: int

class WithdrawalItemCreate(WithdrawalItemBase):
    pass

class WithdrawalItem(WithdrawalItemBase):
    id: uuid.UUID
    item_name: str
    
    class Config:
        from_attributes = True

class WithdrawalBase(BaseModel):
    obra: str
    notes: Optional[str] = None
    warehouse_id: uuid.UUID

class WithdrawalCreate(WithdrawalBase):
    items: List[WithdrawalItemCreate]

class Withdrawal(WithdrawalBase):
    id: uuid.UUID
    withdrawal_date: datetime
    user_id: uuid.UUID
    items: List[WithdrawalItem]
    
    class Config:
        from_attributes = True