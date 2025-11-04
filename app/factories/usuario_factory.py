from app.models.usuario_model import User
from app.schemas.usuario_schema import UserCreate

def build_user_model(data: UserCreate, hashed_password: str) -> User:
    """
    Construye y retorna una instancia de User a partir del schema UserCreate
    y la contraseña hasheada.
    Ajusta los campos si tu modelo tiene más atributos.
    """
    return User(
        email=data.email,
        password=hashed_password,
        display_name=data.display_name
    )