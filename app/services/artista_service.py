from sqlalchemy.orm import Session
from app.models.artista_model import Artist
from app.schemas.artista_schema import ArtistCreate, ArtistResponse
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.dao.artista_dao import get_artista_by_email as dao_get_artista_by_email, create_artista as dao_create_artista
from app.factories.artista_factory import build_artista_model

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def register_artista(data: ArtistCreate, db: Session):
    # Comprobar si el artista ya existe
    existing_artista = dao_get_artista_by_email(db, data.email)
    if existing_artista:
        raise HTTPException(status_code=409, detail="El artista ya existe")
    
    # Hashear contraseña y construir modelo con el factory
    hashed_pw = get_password_hash(data.password)
    new_artista = build_artista_model(data, hashed_pw)

    # Persistir con el DAO
    created = dao_create_artista(db, new_artista)
    return created

def get_artista_by_email(email: str, db: Session):
    artista = dao_get_artista_by_email(db, email)
    if not artista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artista no encontrado")
    return artista