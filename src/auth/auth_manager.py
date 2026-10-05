# src/auth/auth_manager.py
import json
import hashlib
import os
from datetime import datetime
from config import USERS_FILE, DEFAULT_ADMIN, ROLES


class AuthManager:
    """Gestor de autenticación y usuarios del sistema."""
    
    def __init__(self):
        self.users_file = USERS_FILE
        self._ensure_file_exists()
        self.users = self._load_users()
    
    # ---------------------------------------------------------
    # Gestión del archivo de usuarios
    # ---------------------------------------------------------
    def _ensure_file_exists(self):
        """Crea el archivo de usuarios con el admin por defecto si no existe."""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            admin_data = {
                DEFAULT_ADMIN["username"]: {
                    "password": self._hash_password(DEFAULT_ADMIN["password"]),
                    "nombre": DEFAULT_ADMIN["nombre"],
                    "cargo": DEFAULT_ADMIN["cargo"],
                    "rol": DEFAULT_ADMIN["rol"],
                    "estado": DEFAULT_ADMIN["estado"],
                    "fecha_creacion": datetime.now().isoformat(),
                    "ultimo_acceso": None
                }
            }
            self._save_users(admin_data)
    
    def _load_users(self):
        """Carga los usuarios desde el archivo JSON."""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_users(self, users=None):
        """Guarda los usuarios en el archivo JSON."""
        if users is not None:
            self.users = users
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=4, ensure_ascii=False)
    
    # ---------------------------------------------------------
    # Utilidades
    # ---------------------------------------------------------
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hashea la contraseña con SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    # ---------------------------------------------------------
    # Autenticación
    # ---------------------------------------------------------
    def authenticate(self, username: str, password: str):
        """Valida las credenciales del usuario."""
        if username not in self.users:
            return None
        
        user = self.users[username]
        
        if not user.get("estado", False):
            return {"error": "El usuario está deshabilitado"}
        
        if user["password"] != self._hash_password(password):
            return None
        
        # Actualizar último acceso
        self.users[username]["ultimo_acceso"] = datetime.now().isoformat()
        self._save_users()
        
        return {
            "username": username,
            "nombre": user["nombre"],
            "cargo": user.get("cargo", ""),
            "rol": user["rol"]
        }
    
    # ---------------------------------------------------------
    # CRUD de Usuarios
    # ---------------------------------------------------------
    def listar_usuarios(self):
        """Retorna la lista de usuarios sin contraseñas."""
        return [
            {
                "username": username,
                "nombre": data["nombre"],
                "cargo": data.get("cargo", ""),
                "rol": data["rol"],
                "estado": data.get("estado", True),
                "fecha_creacion": data.get("fecha_creacion", ""),
                "ultimo_acceso": data.get("ultimo_acceso", "Nunca")
            }
            for username, data in self.users.items()
        ]
    
    def crear_usuario(self, username, password, nombre, cargo, rol, estado=True):
        """Registra un nuevo usuario."""
        if username in self.users:
            return False, "El nombre de usuario ya existe"
        
        if rol not in ROLES:
            return False, f"Rol inválido. Opciones: {', '.join(ROLES)}"
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        self.users[username] = {
            "password": self._hash_password(password),
            "nombre": nombre,
            "cargo": cargo,
            "rol": rol,
            "estado": estado,
            "fecha_creacion": datetime.now().isoformat(),
            "ultimo_acceso": None
        }
        self._save_users()
        return True, "Usuario creado exitosamente"
    
    def modificar_usuario(self, username, nombre=None, cargo=None, rol=None, 
                          password=None, estado=None):
        """Modifica los datos de un usuario existente."""
        if username not in self.users:
            return False, "El usuario no existe"
        
        user = self.users[username]
        
        if nombre is not None:
            user["nombre"] = nombre
        if cargo is not None:
            user["cargo"] = cargo
        if rol is not None:
            if rol not in ROLES:
                return False, f"Rol inválido. Opciones: {', '.join(ROLES)}"
            user["rol"] = rol
        if password:
            if len(password) < 6:
                return False, "La contraseña debe tener al menos 6 caracteres"
            user["password"] = self._hash_password(password)
        if estado is not None:
            user["estado"] = estado
        
        self._save_users()
        return True, "Usuario modificado exitosamente"
    
    def cambiar_estado(self, username, estado: bool):
        """Habilita o inhabilita un usuario."""
        if username not in self.users:
            return False, "El usuario no existe"
        
        # Evitar deshabilitar al último SuperAdmin activo
        if not estado and self.users[username]["rol"] == "SuperAdmin":
            admins_activos = [
                u for u, d in self.users.items()
                if d["rol"] == "SuperAdmin" and d.get("estado", True)
            ]
            if len(admins_activos) <= 1:
                return False, "No se puede deshabilitar al último SuperAdmin activo"
        
        self.users[username]["estado"] = estado
        self._save_users()
        return True, f"Usuario {'habilitado' if estado else 'deshabilitado'}"
    
    def eliminar_usuario(self, username):
        """Elimina un usuario (solo si no es el último SuperAdmin)."""
        if username not in self.users:
            return False, "El usuario no existe"
        
        if self.users[username]["rol"] == "SuperAdmin":
            admins = [u for u, d in self.users.items() if d["rol"] == "SuperAdmin"]
            if len(admins) <= 1:
                return False, "No se puede eliminar al último SuperAdmin"
        
        del self.users[username]
        self._save_users()
        return True, "Usuario eliminado exitosamente"