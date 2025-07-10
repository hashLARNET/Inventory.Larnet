from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1.endpoints import auth, inventory, withdrawals, warehouses, history
from backend.config import settings
from backend.database.base import engine
from backend.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Multi-Warehouse Inventory System",
    description="Sistema de gestión de inventario multi-bodega",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(warehouses.router, prefix="/api/v1/warehouses", tags=["warehouses"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["inventory"])
app.include_router(withdrawals.router, prefix="/api/v1/withdrawals", tags=["withdrawals"])
app.include_router(history.router, prefix="/api/v1/history", tags=["history"])

@app.get("/")
def read_root():
    return {"message": "Multi-Warehouse Inventory System API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)