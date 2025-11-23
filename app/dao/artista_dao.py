from sqlalchemy.orm import Session
from app.models.artista_model import Artist

def get_artista_by_email(db: Session, email: str):
    return db.query(Artist).filter(Artist.email == email).first()

def create_artista(db: Session, artista: Artist):
    db.add(artista)
    db.commit()
    db.refresh(artista)
    return artista

def update_artista(db: Session, db_artista: Artist, update_data: dict):
    """
    Actualiza los campos de una instancia de Artista.
    """
    for key, value in update_data.items():
        setattr(db_artista, key, value)
    
    db.commit()
    db.refresh(db_artista)
    return db_artista