from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import SECRET_KEY, ALGORITHM
from app.core.database import get_db
from app.dao.usuario_dao import get_user_by_email as dao_get_user_by_email
from app.dao.artista_dao import get_artista_by_email as dao_get_artista_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_identity(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_token(token)
    email = payload.get("sub")
    user_type = payload.get("type")

    if not email or not user_type:
        raise HTTPException(status_code=401, detail="Token sin 'sub' o 'type'")

    if user_type == "user":
        user = dao_get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {
            "user_type": "user",
            "user_data": {
                "email": user.email,
                "display_name": user.display_name,
                "full_name": user.full_name,
                "avatar_url": user.avatar_url,
                "age": user.age,
                "is_admin": user.is_admin,
            },
        }

    if user_type == "artist":
        artist = dao_get_artista_by_email(db, email)
        if not artist:
            raise HTTPException(status_code=404, detail="Artista no encontrado")
        return {
            "user_type": "artist",
            "user_data": {
                "email": artist.email,
                "display_name": artist.display_name,
                "avatar_url": artist.avatar_url,
            },
        }

    raise HTTPException(status_code=400, detail="Tipo de usuario no soportado")