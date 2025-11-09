from app.models.artista_model import Artist
from app.schemas.artista_schema import ArtistCreate

def build_artista_model(data: ArtistCreate, hashed_password: str) -> Artist:
    """
    Construye y retorna una instancia de Artist a partir del schema ArtistCreate
    y la contraseña hasheada.
    """
    return Artist(
        email=data.email,
        password=hashed_password,
        display_name=data.display_name,
        avatar_url=data.avatar_url
    )