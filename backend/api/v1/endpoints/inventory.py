from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from backend.database.session import get_db
from backend.schemas.item import Item, ItemCreate, ItemUpdate
from backend.services.inventory_service import InventoryService
from backend.api.v1.dependencies import get_current_user
from backend.models.user import User

router = APIRouter()

class AddStockRequest(BaseModel):
    quantity: int

@router.post("/items", response_model=Item)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.create_item(item)

@router.post("/items/{item_id}/add_stock", response_model=Item)
def add_stock_to_item(
    item_id: str,
    request: AddStockRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.add_item_stock(item_id, request.quantity, current_user)

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
    warehouse_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.get_items_by_warehouse(warehouse_id, page, per_page)

@router.get("/items/search", response_model=List[Item])
def search_items(
    q: str = Query(..., description="Search query"),
    warehouse_id: Optional[str] = Query(None, description="Filter by warehouse"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.search_items(q, warehouse_id, page, per_page)

@router.get("/items/obra/{obra}/warehouse/{warehouse_id}", response_model=List[Item])
def get_items_by_obra(
    obra: str,
    warehouse_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory_service = InventoryService(db)
    return inventory_service.get_items_by_obra(obra, warehouse_id, page, per_page)