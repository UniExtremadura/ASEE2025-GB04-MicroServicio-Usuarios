from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.models.usuario_model import User
from app.schemas.usuario_schema import UserCreate, UserResponse
from app.dao.usuario_dao import get_user_by_email as dao_get_user_by_email, create_user as dao_create_user
from app.factories.usuario_factory import build_user_model
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str):
    """Hashea una contraseña"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str):
    """Autentica un usuario normal"""
    user = dao_get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def register_user(data: UserCreate, db: Session):
    """Registra un nuevo usuario"""
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
    """Obtiene un usuario por email"""
    user = dao_get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user