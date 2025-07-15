from typing import Dict, Any, Optional

class SessionState:
    def __init__(self):
        self._state: Dict[str, Any] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self._state[key] = value
    
    def clear(self) -> None:
        self._state.clear()
    
    def has(self, key: str) -> bool:
        return key in self._state
    
    @property
    def current_user(self) -> Optional[Dict[str, Any]]:
        return self.get("current_user")
    
    @current_user.setter
    def current_user(self, user: Dict[str, Any]) -> None:
        self.set("current_user", user)
    
    @property
    def current_warehouse(self) -> Optional[Dict[str, Any]]:
        return self.get("current_warehouse")
    
    @current_warehouse.setter
    def current_warehouse(self, warehouse: Dict[str, Any]) -> None:
        self.set("current_warehouse", warehouse)
    
    @property
    def is_authenticated(self) -> bool:
        return self.current_user is not None

# Global session state instance
session_state = SessionState()
