from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://inventory_user:inventory_pass@localhost:5432/inventory_db"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS
    allowed_origins: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()