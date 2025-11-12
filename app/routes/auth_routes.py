from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth_schema import LoginRequest, TokenResponse, MeResponse 
from app.services.usuario_service import authenticate_user, create_access_token
from app.services.artista_service import authenticate_artista
from app.services.auth_service import get_current_identity
from app.core.database import get_db
from datetime import timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Login unificado para usuarios y artistas.
    Intenta autenticar primero como usuario, luego como artista.
    """
    # Intentar autenticar como usuario
    user = authenticate_user(db, credentials.email, credentials.password)
    
    if user:
        # Es un usuario normal
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": user.email, 
                "type": "user"
            },
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_type="user",
            user_data={
                "email": user.email,
                "display_name": user.display_name,
                "full_name": user.full_name,
                "avatar_url": user.avatar_url,
                "age": user.age,
                "is_admin": user.is_admin
            }
        )
    
    # Intentar autenticar como artista
    artist = authenticate_artista(db, credentials.email, credentials.password)
    
    if artist:
        # Es un artista
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": artist.email,
                "type": "artist"
            },
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_type="artist",
            user_data={
                "email": artist.email,
                "display_name": artist.display_name,
                "avatar_url": artist.avatar_url
            }
        )
    
    # Credenciales inválidas
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email o contraseña incorrectos",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/me", response_model=MeResponse)
def me(current = Depends(get_current_identity)):
    return current