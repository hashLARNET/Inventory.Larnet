import requests
import json
from typing import Dict, List, Optional, Any

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"
    
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Login and get user data"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                self.set_token(data["access_token"])
                return data["user"]
            return None
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None
    
    def get_warehouses(self) -> List[Dict[str, Any]]:
        """Get all warehouses"""
        try:
            response = requests.get(
                f"{self.base_url}/warehouses/",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obteniendo bodegas: {e}")
            return []
    
    def get_items_by_warehouse(self, warehouse_id: str, page: int = 1, per_page: int = 50) -> List[Dict[str, Any]]:
        """Get items by warehouse"""
        try:
            params = {"page": page, "per_page": per_page}
            response = requests.get(
                f"{self.base_url}/inventory/items/warehouse/{warehouse_id}",
                headers=self.headers,
                params=params,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obteniendo items: {e}")
            return []
    
    def get_item_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """Get item by barcode"""
        try:
            response = requests.get(
                f"{self.base_url}/inventory/items/barcode/{barcode}",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error buscando item: {e}")
            return None
    
    def search_items(self, query: str, warehouse_id: Optional[str] = None, page: int = 1, per_page: int = 50) -> List[Dict[str, Any]]:
        """Search items"""
        try:
            params = {"q": query, "page": page, "per_page": per_page}
            if warehouse_id:
                params["warehouse_id"] = warehouse_id
            
            response = requests.get(
                f"{self.base_url}/inventory/items/search",
                headers=self.headers,
                params=params,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error buscando items: {e}")
            return []
    
    def create_item(self, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new item"""
        try:
            response = requests.post(
                f"{self.base_url}/inventory/items",
                headers=self.headers,
                json=item_data,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error creando item: {e}")
            return None
    
    def create_withdrawal(self, withdrawal_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create withdrawal"""
        try:
            response = requests.post(
                f"{self.base_url}/withdrawals/",
                headers=self.headers,
                json=withdrawal_data,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error creando retiro: {e}")
            return None
    
    def get_history_by_warehouse(self, warehouse_id: str) -> List[Dict[str, Any]]:
        """Get history by warehouse"""
        try:
            response = requests.get(
                f"{self.base_url}/history/warehouse/{warehouse_id}",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error obteniendo historial: {e}")
            return []