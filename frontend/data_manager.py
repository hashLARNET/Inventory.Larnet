from frontend.api_client import APIClient
from typing import Dict, List, Optional, Any
import uuid

class DataManager:
    def __init__(self):
        self.api_client = APIClient()
        self.current_user = None
        self.current_warehouse = None
    
    def verify_login(self, username: str, password: str) -> bool:
        """Verify login credentials"""
        user = self.api_client.login(username, password)
        if user:
            self.current_user = user
            return True
        return False
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged user"""
        return self.current_user
    
    def set_current_warehouse(self, warehouse: Dict[str, Any]):
        """Set current warehouse"""
        self.current_warehouse = warehouse
    
    def get_current_warehouse(self) -> Optional[Dict[str, Any]]:
        """Get current warehouse"""
        return self.current_warehouse
    
    def get_warehouses(self) -> List[Dict[str, Any]]:
        """Get all warehouses"""
        return self.api_client.get_warehouses()
    
    def get_items(self) -> List[Dict[str, Any]]:
        """Get items from current warehouse"""
        if not self.current_warehouse:
            return []
        return self.api_client.get_items_by_warehouse(str(self.current_warehouse["id"]))
    
    def search_items(self, query: str) -> List[Dict[str, Any]]:
        """Search items in current warehouse"""
        if not self.current_warehouse:
            return []
        return self.api_client.search_items(query, str(self.current_warehouse["id"]))
    
    def get_item_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """Get item by barcode"""
        return self.api_client.get_item_by_barcode(barcode)
    
    def add_item(self, item_data: Dict[str, Any]) -> bool:
        """Add new item"""
        if not self.current_warehouse:
            return False
        
        item_data["warehouse_id"] = str(self.current_warehouse["id"])
        result = self.api_client.create_item(item_data)
        return result is not None
    
    def process_withdrawal(self, items: List[Dict[str, Any]], obra: str, notes: str = "") -> bool:
        """Process withdrawal"""
        if not self.current_warehouse or not items:
            return False
        
        withdrawal_data = {
            "obra": obra,
            "notes": notes,
            "warehouse_id": str(self.current_warehouse["id"]),
            "items": [
                {
                    "item_id": str(item["item"]["id"]),
                    "quantity": item["quantity"]
                }
                for item in items
            ]
        }
        
        result = self.api_client.create_withdrawal(withdrawal_data)
        return result is not None
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get history for current warehouse"""
        if not self.current_warehouse:
            return []
        return self.api_client.get_history_by_warehouse(str(self.current_warehouse["id"]))
    
    def logout(self):
        """Logout user"""
        self.current_user = None
        self.current_warehouse = None
        self.api_client.token = None
        self.api_client.headers = {"Content-Type": "application/json"}