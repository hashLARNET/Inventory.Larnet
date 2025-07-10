from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WithdrawalItemBase(BaseModel):
    item_id: int
    quantity: int

class WithdrawalItemCreate(WithdrawalItemBase):
    pass

class WithdrawalItem(WithdrawalItemBase):
    id: int
    item_name: str
    
    class Config:
        from_attributes = True

class WithdrawalBase(BaseModel):
    obra: str
    notes: Optional[str] = None
    warehouse_id: int

class WithdrawalCreate(WithdrawalBase):
    items: List[WithdrawalItemCreate]

class Withdrawal(WithdrawalBase):
    id: int
    withdrawal_date: datetime
    user_id: int
    items: List[WithdrawalItem]
    
    class Config:
        from_attributes = True