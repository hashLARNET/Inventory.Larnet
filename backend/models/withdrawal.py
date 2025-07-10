from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class Withdrawal(BaseModel):
    __tablename__ = "withdrawals"
    
    withdrawal_date = Column(DateTime, default=datetime.utcnow)
    obra = Column(String(100), nullable=False)
    notes = Column(Text)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="withdrawals")
    warehouse = relationship("Warehouse", back_populates="withdrawals")
    items = relationship("WithdrawalItem", back_populates="withdrawal")

class WithdrawalItem(BaseModel):
    __tablename__ = "withdrawal_items"
    
    quantity = Column(Integer, nullable=False)
    
    # Foreign Keys
    withdrawal_id = Column(Integer, ForeignKey("withdrawals.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    
    # Relationships
    withdrawal = relationship("Withdrawal", back_populates="items")
    item = relationship("Item", back_populates="withdrawal_items")