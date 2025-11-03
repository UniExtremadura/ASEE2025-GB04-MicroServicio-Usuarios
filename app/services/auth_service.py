# app/services/auth_service.py
from app.schemas.usuario_schema import UserCreate, UserResponse

# Base de datos temporal en memoria
fake_db = {}

def register_user(data: UserCreate):
    if data.email in fake_db:
        raise ValueError("El correo ya está registrado")
    user = UserResponse(email=data.email, display_name=data.display_name)
    fake_db[data.email] = user
    return user

def get_user_by_email(email: str):
    return fake_db.get(email)
