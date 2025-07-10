from fastapi import HTTPException, status

class InventoryException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class ItemNotFoundException(HTTPException):
    def __init__(self, item_id: str = None, barcode: str = None):
        if item_id:
            detail = f"Item with ID {item_id} not found"
        elif barcode:
            detail = f"Item with barcode {barcode} not found"
        else:
            detail = "Item not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class InsufficientStockException(HTTPException):
    def __init__(self, item_name: str, available: int, requested: int):
        detail = f"Insufficient stock for {item_name}. Available: {available}, Requested: {requested}"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class WarehouseNotFoundException(HTTPException):
    def __init__(self, warehouse_id: str):
        detail = f"Warehouse with ID {warehouse_id} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnauthorizedWarehouseAccessException(HTTPException):
    def __init__(self):
        detail = "Cannot perform withdrawals from a different warehouse location"
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)