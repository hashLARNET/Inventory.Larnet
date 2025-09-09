from pydantic_settings import BaseSettings
from typing import Optional
from urllib.parse import quote_plus

def encode_database_url(url: str) -> str:
    """Encode special characters in database URL"""
    if '#' in url:
        # Extract password part and encode it
        parts = url.split('@')
        if len(parts) == 2:
            creds_part = parts[0]
            host_part = parts[1]
            # Further split to get password
            if ':' in creds_part:
                protocol_user, password = creds_part.rsplit(':', 1)
                encoded_password = quote_plus(password)
                return f"{protocol_user}:{encoded_password}@{host_part}"
    return url

class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    
    # Database
    database_url: str = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Encode database URL to handle special characters
        if self.database_url:
            self.database_url = encode_database_url(self.database_url)
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080", "http://127.0.0.1:8080"]
    
    class Config:
        env_file = "../.env"

settings = Settings()