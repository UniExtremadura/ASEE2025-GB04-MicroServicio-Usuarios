from typing import List, Optional
from fastapi import APIRouter, Form, File, UploadFile, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.artista_schema import ArtistCreate, ArtistResponse, ArtistUpdate
from app.services.artista_service import register_artista, get_artista_by_email, update_artista_service
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
        avatar_url = None
        if img_perfil:
            avatar_url = await save_avatar(img_perfil, email)
        
        artist_data = ArtistCreate(
            email=email,
            password=password,
            display_name=nombre_artistico,
            avatar_url=avatar_url  
        )
        
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

# --- ENDPOINT PUT (Corregido para usar display_name) ---
@router.put("/{email}", response_model=ArtistResponse)
async def update_artist(
    email: str,
    display_name: Optional[str] = Form(None), 
    password: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        avatar_url = None
        if avatar:
            avatar_url = await save_avatar(avatar, email) 
        
        # Ahora usamos display_name, que coincide con el esquema y la BD
        update_data = ArtistUpdate(
            display_name=display_name, 
            password=password,
            avatar_url=avatar_url 
        )
        
        updated_artist = update_artista_service(email, update_data, db)
        return updated_artist

    except Exception as e:
        print(f"Error actualizando artista: {str(e)}") 
        raise HTTPException(status_code=400, detail=f"Error actualizando: {str(e)}")