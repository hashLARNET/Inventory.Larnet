from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database.session import get_db
from backend.schemas.withdrawal import Withdrawal, WithdrawalCreate
from backend.services.withdrawal_service import WithdrawalService
from backend.api.v1.dependencies import get_current_user
from backend.models.user import User

router = APIRouter()

@router.post("/", response_model=Withdrawal)
def create_withdrawal(
    withdrawal: WithdrawalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    withdrawal_service = WithdrawalService(db)
    return withdrawal_service.create_withdrawal(withdrawal, current_user.id)

@router.get("/warehouse/{warehouse_id}", response_model=List[Withdrawal])
def get_withdrawals_by_warehouse(
    warehouse_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    withdrawal_service = WithdrawalService(db)
    return withdrawal_service.get_withdrawals_by_warehouse(warehouse_id)