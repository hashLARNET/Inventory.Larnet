#!/usr/bin/env python3
"""
Seed script to populate database with sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.base import SessionLocal
from backend.models import Item, Warehouse
import random

def create_sample_items():
    """Create sample items for testing"""
    db = SessionLocal()
    
    try:
        warehouses = db.query(Warehouse).all()
        if not warehouses:
            print("❌ No warehouses found. Run init_db.py first.")
            return
        
        # Sample items data
        items_data = [
            ("Martillo", "Martillo de acero 500g", "7501234567890", 25, 15.50, "Construcción Casa A", "FAC-001"),
            ("Destornillador Phillips", "Destornillador Phillips #2", "7501234567891", 50, 8.75, "Construcción Casa A", "FAC-001"),
            ("Taladro Eléctrico", "Taladro eléctrico 600W", "7501234567892", 8, 125.00, "Construcción Casa B", "FAC-002"),
            ("Tornillos", "Tornillos autorroscantes 3x25mm (caja 100)", "7501234567893", 200, 12.30, "Construcción Casa A", "FAC-001"),
            ("Sierra Manual", "Sierra manual para madera 20\"", "7501234567894", 15, 22.50, "Construcción Casa C", "FAC-003"),
            ("Nivel de Burbuja", "Nivel de burbuja 60cm", "7501234567895", 12, 18.90, "Construcción Casa B", "FAC-002"),
            ("Cinta Métrica", "Cinta métrica 5m", "7501234567896", 30, 9.25, "Construcción Casa A", "FAC-001"),
            ("Alicate", "Alicate universal 8\"", "7501234567897", 20, 14.75, "Construcción Casa C", "FAC-003"),
            ("Llave Inglesa", "Llave inglesa ajustable 10\"", "7501234567898", 18, 16.80, "Construcción Casa B", "FAC-002"),
            ("Soldadora", "Soldadora eléctrica 200A", "7501234567899", 3, 450.00, "Construcción Casa C", "FAC-003")
        ]
        
        for name, description, barcode, stock, price, obra, factura in items_data:
            # Randomly assign to warehouse
            warehouse = random.choice(warehouses)
            
            existing_item = db.query(Item).filter(Item.barcode == barcode).first()
            if not existing_item:
                item = Item(
                    name=name,
                    description=description,
                    barcode=barcode,
                    stock=stock,
                    unit_price=price,
                    obra=obra,
                    n_factura=factura,
                    warehouse_id=warehouse.id
                )
                db.add(item)
                print(f"✅ Item created: {name} in {warehouse.name}")
        
        db.commit()
        print("✅ Sample items created successfully")
        
    except Exception as e:
        print(f"❌ Error creating sample items: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("🌱 Seeding database with sample data...")
    create_sample_items()
    print("\n🎉 Database seeding completed!")

if __name__ == "__main__":
    main()