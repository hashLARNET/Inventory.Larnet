from sqlalchemy.orm import Session
from typing import List, Optional
from backend.models.item import Item
from backend.models.warehouse import Warehouse
from backend.schemas.item import ItemCreate, ItemUpdate
from backend.core.exceptions import ItemNotFoundException, WarehouseNotFoundException
import uuid

class InventoryService:
    def __init__(self, db: Session):
        self.db = db
    
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
            unit_price=item_data.unit_price,
            obra=obra,
            n_factura=n_factura,
            warehouse_id=item_data.warehouse_id
        )
        
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def get_item_by_barcode(self, barcode: str) -> Item:
        item = self.db.query(Item).filter(Item.barcode == barcode).first()
        if not item:
            raise ItemNotFoundException(barcode=barcode)
        return item
    
    def get_items_by_warehouse(self, warehouse_id: str) -> List[Item]:
        return self.db.query(Item).filter(Item.warehouse_id == warehouse_id).all()
    
    def search_items(self, query: str, warehouse_id: Optional[str] = None) -> List[Item]:
        search_query = self.db.query(Item).filter(
            (Item.name.ilike(f"%{query}%")) |
            (Item.n_factura.ilike(f"%{query}%")) |
            (Item.barcode.ilike(f"%{query}%"))
        )
        
        if warehouse_id:
            search_query = search_query.filter(Item.warehouse_id == warehouse_id)
        
        return search_query.all()
    
    def update_item_stock(self, item_id: str, new_stock: int) -> Item:
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            raise ItemNotFoundException(item_id)
        
        item.stock = new_stock
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def get_items_by_obra(self, obra: str, warehouse_id: str) -> List[Item]:
        return self.db.query(Item).filter(
            Item.obra == obra,
            Item.warehouse_id == warehouse_id
        ).all()