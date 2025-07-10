from sqlalchemy import Column, String, Integer, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from .base import BaseModel

class Item(BaseModel):
    __tablename__ = "items"
    
    name = Column(String(200), nullable=False)
    description = Column(Text)
    barcode = Column(String(100), unique=True, nullable=False, index=True)
    stock = Column(Integer, default=0)
    unit_price = Column(Numeric(10, 2))
    obra = Column(String(100), nullable=False)
    n_factura = Column(String(50), nullable=False)
    
    # Foreign Keys
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    
    # Relationships
    warehouse = relationship("Warehouse", back_populates="items")
    withdrawal_items = relationship("WithdrawalItem", back_populates="item")