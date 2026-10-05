# config.py
import os

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# Roles del sistema
ROLES = ["SuperAdmin", "Administrador", "Usuario"]

# Configuración de seguridad
HASH_ALGORITHM = "sha256"
SESSION_TIMEOUT_MINUTES = 30

# Usuario por defecto (solo para primera ejecución)
DEFAULT_ADMIN = {
    "username": "admin",
    "password": "admin123",  # Se hasheará al crear
    "nombre": "Administrador del Sistema",
    "cargo": "Jefe de UTIC",
    "rol": "SuperAdmin",
    "estado": True
}