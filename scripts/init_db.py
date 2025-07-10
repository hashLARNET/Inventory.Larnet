#!/usr/bin/env python3
"""
Database initialization script
Creates tables and initial data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from backend.models import Base, User, Warehouse
from backend.core.security import get_password_hash
from backend.database.base import SessionLocal
from backend.config import settings

def create_tables():
    """Create all database tables"""
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

def create_initial_data():
    """Create initial users and warehouses"""
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = db.query(User).filter(User.username == "Admin_Santiago").first()
        if not admin_user:
            admin_user = User(
                username="Admin_Santiago",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrador Santiago",
                is_admin=True,
                is_active=True
            )
            db.add(admin_user)
            print("✅ Admin user created: Admin_Santiago")
        
        # Create regular users
        users_data = [
            ("Operador_Juan", "juan123", "Juan Pérez"),
            ("Operador_Maria", "maria123", "María González"),
            ("Supervisor_Carlos", "carlos123", "Carlos Rodríguez")
        ]
        
        for username, password, full_name in users_data:
            existing_user = db.query(User).filter(User.username == username).first()
            if not existing_user:
                user = User(
                    username=username,
                    hashed_password=get_password_hash(password),
                    full_name=full_name,
                    is_admin=False,
                    is_active=True
                )
                db.add(user)
                print(f"✅ User created: {username}")
        
        # Create warehouses
        warehouses_data = [
            ("Bodega Principal", "BP001", "Bodega principal del almacén", "Edificio A - Piso 1"),
            ("Bodega Secundaria", "BS002", "Bodega secundaria para overflow", "Edificio B - Piso 2"),
            ("Bodega Herramientas", "BH003", "Bodega especializada en herramientas", "Edificio A - Piso 2")
        ]
        
        for name, code, description, location in warehouses_data:
            existing_warehouse = db.query(Warehouse).filter(Warehouse.code == code).first()
            if not existing_warehouse:
                warehouse = Warehouse(
                    name=name,
                    code=code,
                    description=description,
                    location=location,
                    is_active=True
                )
                db.add(warehouse)
                print(f"✅ Warehouse created: {name}")
        
        db.commit()
        print("✅ Initial data created successfully")
        
    except Exception as e:
        print(f"❌ Error creating initial data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("🚀 Initializing database...")
    
    try:
        create_tables()
        create_initial_data()
        print("\n🎉 Database initialization completed successfully!")
        print("\n📋 Default users created:")
        print("   - Admin_Santiago (password: admin123)")
        print("   - Operador_Juan (password: juan123)")
        print("   - Operador_Maria (password: maria123)")
        print("   - Supervisor_Carlos (password: carlos123)")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()