from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class Warehouse(BaseModel):
    __tablename__ = "warehouses"
    
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    location = Column(String(200))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    items = relationship("Item", back_populates="warehouse")
    withdrawals = relationship("Withdrawal", back_populates="warehouse")