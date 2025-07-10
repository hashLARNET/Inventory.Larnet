import os

class Config:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    APP_TITLE = "Sistema de Inventario Multi-Bodega"
    APP_VERSION = "1.0.0"
    
    # Touch interface settings
    BUTTON_HEIGHT = 60
    BUTTON_WIDTH = 200
    FONT_SIZE_LARGE = 18
    FONT_SIZE_MEDIUM = 14
    FONT_SIZE_SMALL = 12
    
    # Colors
    PRIMARY_COLOR = "#1976D2"
    SECONDARY_COLOR = "#424242"
    SUCCESS_COLOR = "#4CAF50"
    WARNING_COLOR = "#FF9800"
    ERROR_COLOR = "#F44336"
    BACKGROUND_COLOR = "#F5F5F5"

config = Config()