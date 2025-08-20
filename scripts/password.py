#!/usr/bin/env python3
"""
Script para corregir las contraseñas de los usuarios en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.base import SessionLocal
from backend.models.user import User
from backend.core.security import get_password_hash

def fix_user_passwords():
    """Actualizar las contraseñas de todos los usuarios"""
    db = SessionLocal()

    try:
        # Definir usuarios y sus contraseñas
        users_passwords = {
            "RocioLarnet": "RLarNet2022",
            "CatalinaLarnet": "CLarNet2022",
            "JavieraLarnet": "JLarNet2022",
            "InformaticaLarnet": "AILarNet2022"
        }

        for username, password in users_passwords.items():
            user = db.query(User).filter(User.username == username).first()
            if user:
                # Generar hash correcto con bcrypt
                user.hashed_password = get_password_hash(password)
                print(f"✅ Contraseña actualizada para: {username}")
            else:
                # Si el usuario no existe, crearlo
                new_user = User(
                    username=username,
                    hashed_password=get_password_hash(password),
                    fullname=username.replace("", " "),
                    is_admin=(username == "Admin_Santiago"),
                    is_active=True
                )
                db.add(new_user)
                print(f"✅ Usuario creado: {username}")

        db.commit()
        print("\n🎉 Todas las contraseñas han sido actualizadas correctamente")

    except Exception as e:
        print(f"❌ Error actualizando contraseñas: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "main":
    print("🔧 Corrigiendo contraseñas de usuarios...")
    fix_user_passwords()