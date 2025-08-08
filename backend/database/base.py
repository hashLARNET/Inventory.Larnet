from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import settings

engine = create_engine(
    settings.database_url,
    pool_size=10,           # Agregar
    max_overflow=20,        # Agregar
    pool_pre_ping=True,     # Agregar
    pool_recycle=3600       # Agregar
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()