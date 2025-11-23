from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.models.artista_model import Artist
from app.schemas.artista_schema import ArtistCreate, ArtistResponse, ArtistUpdate
from app.dao.artista_dao import (
    get_artista_by_email as dao_get_artista_by_email, 
    create_artista as dao_create_artista,
    update_artista as dao_update_artista
)
from app.factories.artista_factory import build_artista_model
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_artista(db: Session, email: str, password: str):
    artista = dao_get_artista_by_email(db, email)
    if not artista:
        return None
    if not verify_password(password, artista.password):
        return None
    return artista

def register_artista(data: ArtistCreate, db: Session):
    existing_artista = dao_get_artista_by_email(db, data.email)
    if existing_artista:
        raise HTTPException(status_code=409, detail="El artista ya existe")
    hashed_pw = get_password_hash(data.password)
    new_artista = build_artista_model(data, hashed_pw)
    created = dao_create_artista(db, new_artista)
    return created

def get_artista_by_email(email: str, db: Session):
    artista = dao_get_artista_by_email(db, email)
    if not artista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artista no encontrado")
    return artista

# --- FUNCIÓN ACTUALIZADA (FIX NULOS) ---
def update_artista_service(email: str, data: ArtistUpdate, db: Session):
    # 1. Buscar al artista
    artista = dao_get_artista_by_email(db, email)
    if not artista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artista no encontrado")

    # 2. Convertir a diccionario
    update_data = data.dict()

    # ⚠️ FIX CRÍTICO: Eliminar claves con valor None para no sobrescribir datos con NULL
    # Esto protege password, avatar_url y cualquier campo opcional.
    update_data = {k: v for k, v in update_data.items() if v is not None}

    # 3. Hashear password SOLO si viene y no está vacía
    if "password" in update_data:
        pw = update_data["password"]
        if pw and pw.strip(): # Si es string con contenido
            update_data["password"] = get_password_hash(pw)
        else:
            # Si es string vacío, lo quitamos también para no guardar hash de vacío
            del update_data["password"]

    # 4. Guardar
    updated_artista = dao_update_artista(db, artista, update_data)
    
    return updated_artista