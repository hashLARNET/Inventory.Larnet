from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from backend.config import settings

engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=10,           # Agregar
    max_overflow=20,        # Agregar
    pool_pre_ping=True,     # Agregar
    pool_recycle=3600,       # Agregar
    echo_pool=False,        # Debug desactivado
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000"  # 30 segundos timeout
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()