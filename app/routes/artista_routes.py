from typing import List, Optional
from fastapi import APIRouter, Form, File, UploadFile, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.artista_schema import ArtistCreate, ArtistResponse
from app.services.artista_service import register_artista, get_artista_by_email
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
        artist_data = ArtistCreate(
            email=email,
            password=password,
            display_name=nombre_artistico
        )
        artist = register_artista(artist_data, db)

        response = {"success": True, "message": "Artista registrado", "data": {"email": email, "display_name": nombre_artistico}}
        # si hay imagen, procesa y añade avatar_url (placeholder)
        if img_perfil:
            # guardar archivo y setear avatar_url en DB (implementar en servicio)
            pass

        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        return JSONResponse(content={"success": False, "message": "Error interno", "error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/{email}", response_model=ArtistResponse)
def get_artist(email: str, db: Session = Depends(get_db)):
    a = get_artista_by_email(email, db)
    if not a:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return a
