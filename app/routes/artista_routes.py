from typing import List, Optional
from fastapi import APIRouter, Form, File, UploadFile, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.artista_schema import ArtistCreate, ArtistResponse
from app.services.artista_service import register_artista, get_artista_by_email
from app.services.image_service import save_avatar
from app.core.database import get_db

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def registro_form(
    nombre_artistico: str = Form(...),
    email: str = Form(...),
    password: str = Form(...), 
    img_perfil: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        # 👇 Primero guardar la imagen si existe
        avatar_url = None
        if img_perfil:
            avatar_url = await save_avatar(img_perfil, email)
        
        # 👇 Crear el artista CON la URL del avatar
        artist_data = ArtistCreate(
            email=email,
            password=password,
            display_name=nombre_artistico,
            avatar_url=avatar_url  
        )
        
        # Registrar el artista
        artist = register_artista(artist_data, db)

        return {
            "message": "Artista registrado exitosamente",
            "artist": artist
        }
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{email}", response_model=ArtistResponse)
def get_artist(email: str, db: Session = Depends(get_db)):
    artist = get_artista_by_email(email, db)
    if not artist:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artist
