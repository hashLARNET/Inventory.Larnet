from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class History(BaseModel):
    __tablename__ = "history"
    
    action_type = Column(String(50), nullable=False)  # 'withdrawal', 'addition', 'adjustment'
    item_name = Column(String(200), nullable=False)
    quantity = Column(Integer, nullable=False)
    obra = Column(String(100), nullable=False)
    n_factura = Column(String(50), nullable=False)
    warehouse_name = Column(String(100), nullable=False)
    user_name = Column(String(100), nullable=False)
    action_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    
    # Foreign Keys
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    
    # Relationships
    item = relationship("Item")
    user = relationship("User")
    warehouse = relationship("Warehouse")