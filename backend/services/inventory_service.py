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
    
    def get_items_by_warehouse(self, warehouse_id: str, page: int = 1, per_page: int = 1000) -> List[Item]:
        offset = (page - 1) * per_page
        return self.db.query(Item).options(
            joinedload(Item.warehouse)
        ).filter(Item.warehouse_id == warehouse_id).offset(offset).limit(per_page).all()
    
    def search_items(self, query: str, warehouse_id: Optional[str] = None) -> List[Item]:
        search_query = self.db.query(Item).options(
            joinedload(Item.warehouse)
        ).filter(
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
    
    def get_available_obras(self, warehouse_id: str) -> List[str]:
        """Get all available obras in a warehouse"""
        obras = self.db.query(Item.obra).filter(
            Item.warehouse_id == warehouse_id
        ).distinct().all()
        return [obra[0] for obra in obras]

    def get_items_by_obra_detailed(self, warehouse_id: str, obra: str = None) -> List[Item]:
        """Get items by obra with detailed information"""
        query = self.db.query(Item).options(
            joinedload(Item.warehouse)
        ).filter(Item.warehouse_id == warehouse_id)
        
        if obra and obra != "Todas las obras":
            query = query.filter(Item.obra == obra)
        
        return query.all()

    def transfer_item_between_obras(self, item_id: str, from_obra: str, to_obra: str, 
                                   quantity: int, user: User, notes: str = "") -> bool:
        """Transfer items between obras"""
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item or item.stock < quantity:
            return False
        
        # Get warehouse for history
        warehouse = self.db.query(Warehouse).filter(Warehouse.id == item.warehouse_id).first()
        
        # Create new item for destination obra or update existing
        existing_item = self.db.query(Item).filter(
            Item.name == item.name,
            Item.warehouse_id == item.warehouse_id,
            Item.obra == to_obra,
            Item.barcode != item.barcode  # Different barcode for different obra
        ).first()
        
        if existing_item:
            # Update existing item
            existing_item.stock += quantity
        else:
            # Create new item for destination obra
            new_barcode = f"{item.barcode}_{to_obra[:3]}"  # Modify barcode for new obra
            new_item = Item(
                name=item.name,
                description=item.description,
                barcode=new_barcode,
                stock=quantity,
                obra=to_obra,
                n_factura=item.n_factura,
                warehouse_id=item.warehouse_id
            )
            self.db.add(new_item)
        
        # Reduce stock from source item
        item.stock -= quantity
        
        # Add history records
        self.history_service.add_history_record(
            action_type="adjustment",
            item=item,
            quantity=-quantity,
            user=user,
            warehouse=warehouse,
            notes=f"Transferencia desde obra {from_obra} a {to_obra}: {notes}"
        )
        
        self.db.commit()
        return True