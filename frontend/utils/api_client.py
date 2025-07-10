import requests
from typing import Dict, List, Optional, Any
from frontend.config import config

class APIClient:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def set_token(self, token: str):
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/v1/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            self.set_token(data["access_token"])
            return data
        else:
            raise Exception(f"Login failed: {response.text}")
    
    def get_warehouses(self) -> List[Dict[str, Any]]:
        response = requests.get(
            f"{self.base_url}/api/v1/warehouses/",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_items_by_warehouse(self, warehouse_id: str) -> List[Dict[str, Any]]:
        response = requests.get(
            f"{self.base_url}/api/v1/inventory/items/warehouse/{warehouse_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_item_by_barcode(self, barcode: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/api/v1/inventory/items/barcode/{barcode}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def search_items(self, query: str, warehouse_id: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {"q": query}
        if warehouse_id:
            params["warehouse_id"] = warehouse_id
        
        response = requests.get(
            f"{self.base_url}/api/v1/inventory/items/search",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def create_withdrawal(self, withdrawal_data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/v1/withdrawals/",
            headers=self.headers,
            json=withdrawal_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_history_by_warehouse(self, warehouse_id: str) -> List[Dict[str, Any]]:
        response = requests.get(
            f"{self.base_url}/api/v1/history/warehouse/{warehouse_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/v1/inventory/items",
            headers=self.headers,
            json=item_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_items_by_obra(self, obra: str, warehouse_id: str) -> List[Dict[str, Any]]:
        response = requests.get(
            f"{self.base_url}/api/v1/inventory/items/obra/{obra}/warehouse/{warehouse_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Global API client instance
api_client = APIClient()