from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from backend.models.history import History
from backend.models.item import Item
from backend.models.user import User
from backend.models.warehouse import Warehouse

class HistoryService:
    def __init__(self, db: Session):
        self.db = db
    
    def add_history_record(
        self, 
        action_type: str, 
        item: Item, 
        quantity: int, 
        user: User, 
        warehouse: Warehouse,
        notes: Optional[str] = None
    ) -> History:
        history_record = History(
            action_type=action_type,
            item_name=item.name,
            quantity=quantity,
            obra=item.obra,
            n_factura=item.n_factura,
            warehouse_name=warehouse.name,
            user_name=user.full_name,
            action_date=datetime.utcnow(),
            notes=notes,
            item_id=item.id,
            user_id=user.id,
            warehouse_id=warehouse.id
        )
        
        self.db.add(history_record)
        self.db.commit()
        self.db.refresh(history_record)
        return history_record
    
    def get_history_by_warehouse(self, warehouse_id: int) -> List[History]:
        return self.db.query(History).filter(
            History.warehouse_id == warehouse_id
        ).order_by(History.action_date.desc()).all()
    
    def get_history_by_item(self, item_id: int) -> List[History]:
        return self.db.query(History).filter(
            History.item_id == item_id
        ).order_by(History.action_date.desc()).all()
    
    def get_all_history(self) -> List[History]:
        return self.db.query(History).order_by(History.action_date.desc()).all()