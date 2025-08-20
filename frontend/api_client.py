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
    
    def get_items_by_warehouse(self, warehouse_id: str) -> List[Dict[str, Any]]:
        """Get items by warehouse"""
        try:
            response = requests.get(
                f"{self.base_url}/inventory/items/warehouse/{warehouse_id}",
                headers=self.headers,
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
    
    def search_items(self, query: str, warehouse_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search items"""
        try:
            params = {"q": query}
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
        

    def send_history_report_email(self, receiver_email: str, subject: str = None, 
                                body: str = None, warehouse_name: str = None,
                                warehouse_id: str = None) -> Dict[str, Any]:
        """Send history report email through backend API"""
        try:
            payload = {
                "receiver_email": receiver_email,
                "subject": subject,
                "body": body,
                "warehouse_name": warehouse_name,
                "warehouse_id": warehouse_id
            }
            
            # Remove None values from payload
            payload = {k: v for k, v in payload.items() if v is not None}
            
            response = requests.post(
                f"{self.base_url}/email/send-history-report",
                headers=self.headers,
                json=payload,
                timeout=60  # Longer timeout for email operations
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "message": f"Error del servidor: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {"success": False, "message": "Timeout: La operación de email tardó demasiado"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "message": "Error de conexión: No se pudo conectar al servidor"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Error de red: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"Error inesperado: {str(e)}"}
    
    def check_email_service(self) -> Dict[str, Any]:
        """Check if email service is available"""
        try:
            response = requests.get(
                f"{self.base_url}/email/health",
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Email service unavailable: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

        
    