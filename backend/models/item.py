from sqlalchemy import Column, String, Integer, ForeignKey, Text, Numeric, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import BaseModel

class Item(BaseModel):
    __tablename__ = "items"
    
    name = Column(String(200), nullable=False)
    description = Column(Text)
    barcode = Column(String(100), unique=True, nullable=False, index=True)
    stock = Column(Integer, default=0)
    obra = Column(String(100), nullable=False)
    n_factura = Column(String(50), nullable=False)
    
    # Foreign Keys
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=False)
    
    # Relationships
    warehouse = relationship("Warehouse", back_populates="items")
    withdrawal_items = relationship("WithdrawalItem", back_populates="item")

    __table_args__ = (
        Index('idx_warehouse_obra', 'warehouse_id', 'obra'),  # Para búsquedas por bodega+obra
        Index('idx_name_barcode', 'name', 'barcode'),        # Para búsquedas de texto
    )