from sqlalchemy.orm import Session
from app.models.usuario_model import User
from app.schemas.usuario_schema import UserCreate, UserResponse
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.dao.usuario_dao import get_user_by_email as dao_get_user_by_email, create_user as dao_create_user
from app.factories.usuario_factory import build_user_model

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def register_user(data: UserCreate, db: Session):
    # Comprobar si el usuario ya existe
    existing_user = dao_get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

    # Hashear contraseña y construir modelo con el factory
    hashed_pw = get_password_hash(data.password)
    new_user = build_user_model(data, hashed_pw)

    # Persistir con el DAO
    created = dao_create_user(db, new_user)
    return created

def get_user_by_email(email: str, db: Session):
    user = dao_get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user