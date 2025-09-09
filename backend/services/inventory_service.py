from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List, Optional, Tuple
from functools import lru_cache
from backend.models.item import Item
from backend.models.warehouse import Warehouse
from backend.models.user import User
from backend.schemas.item import ItemCreate, ItemUpdate
from backend.core.exceptions import ItemNotFoundException, WarehouseNotFoundException
from backend.services.history_service import HistoryService
import uuid


class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.history_service = HistoryService(db)
    
    @lru_cache(maxsize=32)
    def _get_warehouse_cached(self, warehouse_id: str) -> Optional[Tuple[str, str, str]]:
        """Cache warehouse data since it changes rarely"""
        warehouse = self.db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
        return (warehouse.id, warehouse.name, warehouse.code) if warehouse else None
    
    def create_item(self, item_data: ItemCreate) -> Item:
        # Verify warehouse exists
        warehouse = self.db.query(Warehouse).filter(Warehouse.id == item_data.warehouse_id).first()
        if not warehouse:
            raise WarehouseNotFoundException(item_data.warehouse_id)
        
        # If no obra or n_factura provided, use warehouse as default
        obra = item_data.obra if item_data.obra else warehouse.name
        n_factura = item_data.n_factura if item_data.n_factura else warehouse.code
        
        db_item = Item(
            name=item_data.name,
            description=item_data.description,
            barcode=item_data.barcode,
            stock=item_data.stock,
            obra=obra,
            n_factura=n_factura,
            warehouse_id=item_data.warehouse_id
        )
        
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def add_item_stock(self, item_id: str, quantity: int, user: User) -> Item:
        """Add stock to an existing item"""
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ItemNotFoundException(item_id)
        
        # Get warehouse for history
        warehouse = self.db.query(Warehouse).filter(Warehouse.id == item.warehouse_id).first()
        
        # Update stock
        item.stock += quantity
        self.db.commit()
        self.db.refresh(item)
        
        # Add to history
        self.history_service.add_history_record(
            action_type="addition",
            item=item,
            quantity=quantity,
            user=user,
            warehouse=warehouse,
            notes=f"Stock agregado: +{quantity} unidades"
        )
        
        return item
    
    def get_item_by_barcode(self, barcode: str) -> Item:
        item = self.db.query(Item).filter(Item.barcode == barcode).first()
        if not item:
            raise ItemNotFoundException(barcode=barcode)
        return item
    
    def get_items_by_warehouse(self, warehouse_id: str, page: int = 1, per_page: int = 50) -> List[Item]:
        offset = (page - 1) * per_page
        return self.db.query(Item).options(
            joinedload(Item.warehouse)  # Evita N+1 queries
        ).filter(Item.warehouse_id == warehouse_id).offset(offset).limit(per_page).all()
    
    def search_items(self, query: str, warehouse_id: Optional[str] = None, page: int = 1, per_page: int = 50) -> List[Item]:
        offset = (page - 1) * per_page
        search_query = self.db.query(Item).options(
            joinedload(Item.warehouse)
        ).filter(
            (Item.name.ilike(f"%{query}%")) |
            (Item.n_factura.ilike(f"%{query}%")) |
            (Item.barcode.ilike(f"%{query}%"))
        )
        
        if warehouse_id:
            search_query = search_query.filter(Item.warehouse_id == warehouse_id)
        
        return search_query.offset(offset).limit(per_page).all()
    
    def update_item_stock(self, item_id: str, new_stock: int) -> Item:
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ItemNotFoundException(item_id)
        
        item.stock = new_stock
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def get_items_by_obra(self, obra: str, warehouse_id: str, page: int = 1, per_page: int = 50) -> List[Item]:
        offset = (page - 1) * per_page
        return self.db.query(Item).filter(
            Item.obra == obra,
            Item.warehouse_id == warehouse_id
        ).offset(offset).limit(per_page).all()