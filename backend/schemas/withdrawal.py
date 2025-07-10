from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WithdrawalItemBase(BaseModel):
    item_id: str
    quantity: int

class WithdrawalItemCreate(WithdrawalItemBase):
    pass

class WithdrawalItem(WithdrawalItemBase):
    id: str
    item_name: str
    
    class Config:
        from_attributes = True

class WithdrawalBase(BaseModel):
    obra: str
    notes: Optional[str] = None
    warehouse_id: str

class WithdrawalCreate(WithdrawalBase):
    items: List[WithdrawalItemCreate]

class Withdrawal(WithdrawalBase):
    id: str
    withdrawal_date: datetime
    user_id: str
    items: List[WithdrawalItem]
    
    class Config:
        from_attributes = True