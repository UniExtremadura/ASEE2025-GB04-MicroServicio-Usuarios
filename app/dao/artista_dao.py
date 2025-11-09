from sqlalchemy.orm import Session
from app.models.artista_model import Artist

def get_artista_by_email(db: Session, email: str):
    """
    Retorna una instancia Artist o None.
    """
    return db.query(Artist).filter(Artist.email == email).first()


def create_artista(db: Session, artista: Artist):
    """
    Crea un nuevo artista en la base de datos.
    """
    db.add(artista)
    db.commit()
    db.refresh(artista)
    return artista
