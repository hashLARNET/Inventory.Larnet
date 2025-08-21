#!/usr/bin/env python3
"""
Script para actualizar las contraseñas de los usuarios en la base de datos Supabase
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.base import SessionLocal
from backend.models.user import User
from backend.core.security import get_password_hash

def fix_user_passwords():
    """Actualizar las contraseñas de todos los usuarios según tus especificaciones"""
    db = SessionLocal()

    try:
        # Definir usuarios y sus contraseñas según tu configuración
        users_passwords = {
            "RocioLarnet": "RLarNet2022",
            "CatalinaLarnet": "CLarNet2022",
            "JavieraLarnet": "JLarNet2022",
            "InformaticaLarnet": "AILarNet2022",
            "BastianLarnet": "BLarNet2022",
            "AldoLarnet": "ALarNet2022",
            "AlvaroLarnet": "AGLarNet2022"
        }

        print("🔧 Actualizando contraseñas de usuarios LarNet...")
        
        for username, password in users_passwords.items():
            user = db.query(User).filter(User.username == username).first()
            if user:
                # Generar hash correcto con bcrypt
                new_hash = get_password_hash(password)
                user.hashed_password = new_hash
                print(f"✅ Contraseña actualizada para: {username}")
                print(f"   Nuevo hash: {new_hash[:50]}...")
            else:
                # Si el usuario no existe, crearlo
                # InformaticaLarnet será admin, el resto usuarios normales
                is_admin = (username == "InformaticaLarnet")
                
                # Mapear nombres completos
                full_names = {
                    "RocioLarnet": "Rocío Cifuentes",
                    "CatalinaLarnet": "Catalina Vaus",
                    "JavieraLarnet": "Javiera Pavez",
                    "InformaticaLarnet": "Area de Informatica y Telecomunicaciones",
                    "BastianLarnet": "Bastián Farias",
                    "AldoLarnet": "Aldo Pavez",
                    "AlvaroLarnet": "Álvaro Gallardo"
                }
                
                new_user = User(
                    username=username,
                    hashed_password=get_password_hash(password),
                    full_name=full_names.get(username, username),
                    is_admin=is_admin,
                    is_active=True
                )
                db.add(new_user)
                admin_status = " (ADMINISTRADOR)" if is_admin else ""
                print(f"✅ Usuario creado: {username}{admin_status}")

        db.commit()
        print("\n🎉 Todas las contraseñas han sido actualizadas correctamente")
        print("\n📋 Usuarios disponibles:")
        print("   - RocioLarnet / RLarNet2022")
        print("   - CatalinaLarnet / CLarNet2022")
        print("   - JavieraLarnet / JLarNet2022")
        print("   - InformaticaLarnet / AILarNet2022 (👑 ADMIN)")
        print("   - BastianLarnet / BLarNet2022")
        print("   - AldoLarnet / ALarNet2022")
        print("   - AlvaroLarnet / AGLarNet2022")

    except Exception as e:
        print(f"❌ Error actualizando contraseñas: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_login():
    """Probar login con los usuarios actualizados"""
    from backend.core.security import verify_password
    
    db = SessionLocal()
    try:
        print("\n🧪 Probando autenticación de usuarios...")
        
        # Probar cada usuario con su contraseña
        test_credentials = [
            ("RocioLarnet", "RLarNet2022"),
            ("CatalinaLarnet", "CLarNet2022"),
            ("JavieraLarnet", "JLarNet2022"),
            ("InformaticaLarnet", "AILarNet2022"),
            ("BastianLarnet", "BLarNet2022"),
            ("AldoLarnet", "ALarNet2022"),
            ("AlvaroLarnet", "AGLarNet2022")
        ]
        
        for username, password in test_credentials:
            user = db.query(User).filter(User.username == username).first()
            if user:
                is_valid = verify_password(password, user.hashed_password)
                admin_indicator = " 👑" if user.is_admin else ""
                status = "✅ CORRECTO" if is_valid else "❌ INCORRECTO"
                print(f"   {username}{admin_indicator}: {status}")
            else:
                print(f"   {username}: ❌ USUARIO NO ENCONTRADO")
                
    except Exception as e:
        print(f"❌ Error probando login: {e}")
    finally:
        db.close()

def verify_database_connection():
    """Verificar que la conexión a la base de datos funciona"""
    try:
        from backend.config import settings
        print("🔍 Verificando configuración de base de datos...")
        print(f"   URL: {settings.database_url[:50]}..." if settings.database_url else "No configurada")
        
        db = SessionLocal()
        # Probar una consulta simple
        users_count = db.query(User).count()
        print(f"   ✅ Conexión exitosa - {users_count} usuarios en la base de datos")
        db.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False

def clean_old_users():
    """Limpiar usuarios antiguos que ya no se usan"""
    db = SessionLocal()
    try:
        print("\n🧹 Limpiando usuarios antiguos...")
        
        # Lista de usuarios antiguos que deben ser eliminados
        old_users = ["Admin_Santiago", "Operador_Juan", "Operador_Maria", "Supervisor_Carlos"]
        
        for old_username in old_users:
            old_user = db.query(User).filter(User.username == old_username).first()
            if old_user:
                db.delete(old_user)
                print(f"   🗑️  Usuario eliminado: {old_username}")
        
        db.commit()
        print("   ✅ Limpieza completada")
        
    except Exception as e:
        print(f"   ❌ Error en limpieza: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando script de configuración para usuarios LarNet...")
    
    # Verificar conexión primero
    if not verify_database_connection():
        print("❌ No se puede continuar sin conexión a la base de datos")
        sys.exit(1)
    
    # Limpiar usuarios antiguos
    clean_old_users()
    
    # Actualizar contraseñas
    fix_user_passwords()
    
    # Probar login
    test_login()
    
    print("\n✨ Script completado. Ahora puedes iniciar sesión en la aplicación con cualquier usuario LarNet.")
    print("🚀 Para iniciar la aplicación ejecuta:")
    print("   python frontend/app.py")