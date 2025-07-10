from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database.session import get_db
from backend.schemas.item import Item, ItemCreate, ItemUpdate
from backend.services.inventory_service import InventoryService
from backend.api.v1.dependencies import get_current_user
from backend.models.user import User

router = APIRouter()

@router.post("/items", response_model=Item)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.create_item(item)

@router.get("/items/barcode/{barcode}", response_model=Item)
def get_item_by_barcode(
    barcode: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.get_item_by_barcode(barcode)

@router.get("/items/warehouse/{warehouse_id}", response_model=List[Item])
def get_items_by_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.get_items_by_warehouse(warehouse_id)

@router.get("/items/search", response_model=List[Item])
def search_items(
    q: str = Query(..., description="Search query"),
    warehouse_id: Optional[int] = Query(None, description="Filter by warehouse"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.search_items(q, warehouse_id)

@router.get("/items/obra/{obra}/warehouse/{warehouse_id}", response_model=List[Item])
def get_items_by_obra(
    obra: str,
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.get_items_by_obra(obra, warehouse_id)