class InventoryConfig:
    """Configuración para las nuevas funcionalidades de inventario"""
    
    # Configuración de alertas de stock
    LOW_STOCK_THRESHOLD = 10
    CRITICAL_STOCK_THRESHOLD = 5
    HIGH_STOCK_THRESHOLD = 100
    
    # Configuración de transferencias
    MAX_TRANSFER_QUANTITY = 9999
    REQUIRE_TRANSFER_NOTES = False
    AUTO_CREATE_BARCODE_FOR_TRANSFERS = True
    
    # Configuración de vistas
    DEFAULT_VIEW_MODE = "detallado"
    ITEMS_PER_PAGE = 50
    ENABLE_PAGINATION = True
    
    # Configuración de exportación
    EXPORT_FORMATS = ["csv", "excel"]
    DEFAULT_EXPORT_FORMAT = "csv"
    
    # Configuración de búsqueda
    MIN_SEARCH_LENGTH = 2
    SEARCH_DELAY_MS = 300
    
    # Configuración de colores para estados
    COLORS = {
        'no_stock': '#ffeeee',
        'low_stock': '#fff7e6',
        'normal_stock': '#f0fff0',
        'high_stock': '#e6ffe6',
        'critical_stock': '#ffe6e6'
    }
    
    # Mensajes de confirmación
    CONFIRMATION_MESSAGES = {
        'transfer': "¿Está seguro de realizar esta transferencia?\nEsta acción no se puede deshacer.",
        'delete': "¿Está seguro de eliminar este elemento?",
        'bulk_action': "¿Está seguro de realizar esta acción en {count} elementos?"
    }