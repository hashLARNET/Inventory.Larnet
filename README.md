# Sistema de Inventario Multi-Bodega

Sistema de gestión de inventario con soporte para múltiples bodegas, control de retiros mediante código de barras y trazabilidad completa.

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
- **Frontend**: Streamlit/Flet
- **Base de datos**: PostgreSQL
- **Autenticación**: JWT
- **Contenedores**: Docker

## 📋 Requisitos

- Python 3.9+
- PostgreSQL 13+
- Docker (opcional)

## 🚀 Instalación

1. Clonar el repositorio:
\`\`\`bash
git clone https://github.com/tu-usuario/inventario-system.git
cd inventario-system
\`\`\`

2. Crear entorno virtual:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
\`\`\`

3. Instalar dependencias:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Configurar variables de entorno:
\`\`\`bash
cp .env.example .env
# Editar .env con tus configuraciones
\`\`\`

5. Inicializar base de datos:
\`\`\`bash
python scripts/init_db.py
\`\`\`

## 🎮 Uso

### Backend
\`\`\`bash
cd backend
uvicorn main:app --reload
\`\`\`

### Frontend
\`\`\`bash
cd frontend
streamlit run app.py
\`\`\`

## 📚 Documentación

- API Documentation: http://localhost:8000/docs
- [Guía de Usuario](docs/USER_GUIDE.md)
- [Documentación API](docs/API.md)

## 🤝 Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para detalles.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.
