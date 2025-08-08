from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List
from datetime import datetime
from backend.models.withdrawal import Withdrawal, WithdrawalItem
from backend.models.item import Item
from backend.models.user import User
from backend.models.warehouse import Warehouse
from backend.schemas.withdrawal import WithdrawalCreate
from backend.schemas.withdrawal import Withdrawal as WithdrawalSchema, WithdrawalItem as WithdrawalItemSchema
from backend.services.history_service import HistoryService
from backend.core.exceptions import (
    ItemNotFoundException, 
    InsufficientStockException,
    WarehouseNotFoundException
)

class WithdrawalService:
    def __init__(self, db: Session):
        self.db = db
        self.history_service = HistoryService(db)
    
    def create_withdrawal(self, withdrawal_data: WithdrawalCreate, user_id: str) -> WithdrawalSchema:
        # Verify warehouse exists
        warehouse = self.db.query(Warehouse).options(
        selectinload(Warehouse.items)  # Pre-cargar items si los necesitas
        ).filter(Warehouse.id == withdrawal_data.warehouse_id).first()
        
        # Create withdrawal record
        db_withdrawal = Withdrawal(
            obra=withdrawal_data.obra,
            notes=withdrawal_data.notes,
            user_id=user_id,
            warehouse_id=withdrawal_data.warehouse_id,
            withdrawal_date=datetime.utcnow()
        )
        
        self.db.add(db_withdrawal)
        self.db.flush()  # Get the ID without committing
        
        # Process each item in the withdrawal
        item_ids = [item_data.item_id for item_data in withdrawal_data.items]
        items = self.db.query(Item).options(
            joinedload(Item.warehouse)
        ).filter(Item.id.in_(item_ids)).all()
        items_dict = {str(item.id): item for item in items}

        for item_data in withdrawal_data.items:
            item = items_dict.get(str(item_data.item_id))
            
            # Check if item belongs to the same warehouse
            if item.warehouse_id != withdrawal_data.warehouse_id:
                raise Exception(f"Item {item.name} does not belong to warehouse {warehouse.name}")
            
            # Check stock availability
            if item.stock < item_data.quantity:
                raise InsufficientStockException(item.name, item.stock, item_data.quantity)
            
            # Create withdrawal item record
            withdrawal_item = WithdrawalItem(
                withdrawal_id=db_withdrawal.id,
                item_id=item.id,
                quantity=item_data.quantity
            )
            self.db.add(withdrawal_item)
            
            # Update item stock
            item.stock -= item_data.quantity
            
            # Add to history
            user = self.db.query(User).filter(User.id == user_id).first()
            self.history_service.add_history_record(
                action_type="withdrawal",
                item=item,
                quantity=item_data.quantity,
                user=user,
                warehouse=warehouse,
                notes=f"Withdrawal for obra: {withdrawal_data.obra}"
            )
        
        self.db.commit()
        self.db.refresh(db_withdrawal)
        return self.convert_to_withdrawal_schema(db_withdrawal)
    

    def convert_to_withdrawal_schema(self, withdrawal: Withdrawal) -> WithdrawalSchema:
        return WithdrawalSchema(
            id=withdrawal.id,
            obra=withdrawal.obra,
            notes=withdrawal.notes,
            warehouse_id=withdrawal.warehouse_id,
            withdrawal_date=withdrawal.withdrawal_date,
            user_id=withdrawal.user_id,
            items=[
                WithdrawalItemSchema(
                    id=item.id,
                    item_id=item.item_id,
                    quantity=item.quantity,
                    item_name=item.item.name
                ) for item in withdrawal.items
            ]
        )


    def get_withdrawals_by_warehouse(self, warehouse_id: str) -> List[WithdrawalSchema]:
        return self.db.query(Withdrawal).filter(Withdrawal.warehouse_id == warehouse_id).all()
    
    def can_withdraw_from_warehouse(self, user_warehouse_id: str, target_warehouse_id: str) -> bool:
        """US5: Only allow withdrawals from physical location"""
        return user_warehouse_id == target_warehouse_id
    
    