# Sistema de Inventario Multi-Bodega

Sistema de gestión de inventario con soporte para múltiples bodegas, control de retiros mediante código de barras y trazabilidad completa.

## 🗄️ Base de Datos

Este proyecto utiliza **Supabase** como base de datos. Supabase proporciona:
- PostgreSQL con extensiones avanzadas
- Autenticación integrada
- API REST automática
- Interfaz de administración web
- Escalabilidad automática

## 🌟 Características

- ✅ Gestión multi-bodega
- ✅ Control de inventario en tiempo real
- ✅ Sistema de retiros con código de barras
- ✅ Asignación de items a obras y facturas
- ✅ Historial completo de movimientos
- ✅ Interfaz táctil optimizada
- ✅ Sistema de autenticación

## 🛠️ Tecnologías

- **Backend**: FastAPI + SQLAlchemy
- **Frontend**: Tkinter
- **Base de datos**: Supabase (PostgreSQL)
- **Autenticación**: JWT
- **Contenedores**: Docker

## 📋 Requisitos

- Python 3.9+
- Cuenta de Supabase
- Docker (opcional)

## 🚀 Instalación

### 1. Configurar Supabase

1. Crear cuenta en [Supabase](https://supabase.com)
2. Crear nuevo proyecto
3. Ir a Settings > API para obtener:
   - Project URL
   - Anon key
   - Service role key
4. Ejecutar las migraciones SQL en el editor SQL de Supabase:
   - `supabase/migrations/create_users_table.sql`
   - `supabase/migrations/create_warehouses_table.sql`
   - `supabase/migrations/create_items_table.sql`
   - `supabase/migrations/create_withdrawals_table.sql`
   - `supabase/migrations/create_history_table.sql`
   - `supabase/migrations/insert_initial_data.sql`

### 2. Configurar Proyecto Local

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/inventario-system.git
cd inventario-system
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones de Supabase
```

Ejemplo de `.env`:
```bash
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key
DATABASE_URL=postgresql://postgres:tu-password@db.tu-proyecto.supabase.co:5432/postgres
SECRET_KEY=tu-secret-key-super-seguro
```

**NOTA IMPORTANTE**: Si tu contraseña de base de datos contiene caracteres especiales como `#`, el sistema los codificará automáticamente.

## 👥 Usuarios Predeterminados

El sistema viene con usuarios predeterminados (contraseña para todos: `admin123`):

- **Admin_Santiago** - Administrador del sistema
- **Operador_Juan** - Operador de bodega
- **Operador_Maria** - Operador de bodega  
- **Supervisor_Carlos** - Supervisor de bodega

## 🎮 Uso

### Backend
```bash
cd backend
uvicorn main:app --reload
```

O desde el directorio raíz:
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
python frontend/app.py
```

## 🏗️ Estructura de Base de Datos

### Tablas Principales:
- **users**: Gestión de usuarios y autenticación
- **warehouses**: Información de bodegas
- **items**: Inventario de productos
- **withdrawals**: Registros de retiros
- **withdrawal_items**: Detalle de items retirados
- **history**: Historial completo de movimientos

## 📚 Documentación

- API Documentation: http://localhost:8000/docs
- [Guía de Usuario](docs/USER_GUIDE.md)
- [Documentación API](docs/API.md)

## 🤝 Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para detalles.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.
