from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database.session import get_db
from backend.schemas.history import History
from backend.services.history_service import HistoryService
from backend.api.v1.dependencies import get_current_user
from backend.models.user import User

router = APIRouter()

@router.get("/warehouse/{warehouse_id}", response_model=List[History])
def get_history_by_warehouse(
    warehouse_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history_service = HistoryService(db)
    return history_service.get_history_by_warehouse(warehouse_id)

@router.get("/item/{item_id}", response_model=List[History])
def get_history_by_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history_service = HistoryService(db)
    return history_service.get_history_by_item(item_id)

@router.get("/", response_model=List[History])
def get_all_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    history_service = HistoryService(db)
    return history_service.get_all_history()