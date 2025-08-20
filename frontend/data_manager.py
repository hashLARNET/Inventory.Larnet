from frontend.api_client import APIClient
from typing import Dict, List, Optional, Any
import uuid

class DataManager:
    def __init__(self):
        self.api_client = APIClient()
        self.current_user = None
        self.current_warehouse = None
    
    def verify_login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Verify login credentials"""
        user = self.api_client.login(username, password)
        if user:
            self.current_user = user
            return user
        return None
    
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
    
    def get_items_by_warehouse(self, warehouse_id: str) -> List[Dict[str, Any]]:
        """Get items from specific warehouse"""
        return self.api_client.get_items_by_warehouse(warehouse_id)
    
    def search_items(self, query: str, warehouse_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search items in warehouse"""
        return self.api_client.search_items(query, warehouse_id)
    
    def get_item_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """Get item by barcode"""
        return self.api_client.get_item_by_barcode(barcode)
    
    def get_items_by_obra(self, obra: str, warehouse_id: str) -> List[Dict[str, Any]]:
        """Get items by specific obra"""
        return self.api_client.get_items_by_obra(obra, warehouse_id)
    
    def add_item(self, item_data: Dict[str, Any]) -> bool:
        """Add new item"""
        # Remove unit_price if it exists
        if 'unit_price' in item_data:
            del item_data['unit_price']
        result = self.api_client.create_item(item_data)
        return result is not None
    
    def add_item_stock(self, item_id: str, quantity: int) -> bool:
        """Add stock to existing item"""
        try:
            import requests
            headers = {"Authorization": f"Bearer {self.api_client.token}"}
            response = requests.post(
                f"{self.api_client.base_url}/inventory/items/{item_id}/add_stock",
                headers=headers,
                json={"quantity": quantity},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error agregando stock: {e}")
            return False
    
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
    
    def get_obras_by_warehouse(self, warehouse_id: str) -> List[str]:
        """Get available obras in warehouse"""
        return self.api_client.get_obras_by_warehouse(warehouse_id)

    def transfer_item_between_obras(self, item_id: str, from_obra: str, to_obra: str, 
                                   quantity: int, notes: str = "") -> bool:
        """Transfer item between obras"""
        transfer_data = {
            "item_id": item_id,
            "from_obra": from_obra,
            "to_obra": to_obra,
            "quantity": quantity,
            "notes": notes
        }
        return self.api_client.transfer_item_between_obras(transfer_data)
    
    def get_warehouse_statistics(self, warehouse_id: str) -> Dict[str, Any]:
        """Get warehouse statistics"""
        items = self.get_items_by_warehouse(warehouse_id)
        
        if not items:
            return {
                'total_items': 0,
                'total_stock': 0,
                'obras_count': 0,
                'low_stock_items': 0,
                'no_stock_items': 0,
                'top_obras': []
            }
        
        # Calcular estadísticas
        total_items = len(items)
        total_stock = sum(item['stock'] for item in items)
        obras = list(set(item['obra'] for item in items))
        obras_count = len(obras)
        low_stock_items = len([item for item in items if 0 < item['stock'] < 10])
        no_stock_items = len([item for item in items if item['stock'] == 0])
        
        # Top obras por cantidad de items
        obras_summary = {}
        for item in items:
            obra = item['obra']
            if obra not in obras_summary:
                obras_summary[obra] = {'items': 0, 'stock': 0}
            obras_summary[obra]['items'] += 1
            obras_summary[obra]['stock'] += item['stock']
        
        top_obras = sorted(
            obras_summary.items(),
            key=lambda x: x[1]['stock'],
            reverse=True
        )[:5]
        
        return {
            'total_items': total_items,
            'total_stock': total_stock,
            'obras_count': obras_count,
            'low_stock_items': low_stock_items,
            'no_stock_items': no_stock_items,
            'top_obras': top_obras
        }
    
    def send_history_report_email(self, receiver_email: str, subject: str = None, 
                                body: str = None, warehouse_name: str = None,
                                warehouse_id: str = None) -> Dict[str, Any]:
        """Send history report email - CORREGIDO: ahora acepta warehouse_id"""
        # Si no se proporciona warehouse_id, usar el current_warehouse
        if warehouse_id is None and self.current_warehouse:
            warehouse_id = str(self.current_warehouse['id'])
        
        return self.api_client.send_history_report_email(
            receiver_email=receiver_email,
            subject=subject,
            body=body,
            warehouse_name=warehouse_name,
            warehouse_id=warehouse_id
        )
    
    def check_email_service(self) -> Dict[str, Any]:
        """Check if email service is available"""
        return self.api_client.check_email_service()


    def logout(self):
        """Logout user"""
        self.current_user = None
        self.current_warehouse = None
        self.api_client.token = None
        self.api_client.headers = {"Content-Type": "application/json"}