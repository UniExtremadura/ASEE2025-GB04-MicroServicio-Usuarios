from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UserCreate, UserResponse
from app.services.auth_service import register_user,get_user_by_email
from app.core.database import get_db

router = APIRouter()
    
# Nuevo endpoint para el formulario con imagen
@router.post("/registro", status_code=status.HTTP_201_CREATED)
async def registro_completo(
    usuario: str = Form(...),
    nombre_completo: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    edad: int = Form(...),
    img_perfil: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        # Crear el objeto UserCreate con los datos del formulario
        user_data = UserCreate(
            email=email,
            password=password,
            display_name=nombre_completo,
            full_name=nombre_completo,
            age=edad
        )
        
        # Registrar el usuario
        user = register_user(user_data, db)
        
        # Si hay imagen, procesarla aquí
        if img_perfil:
            # Aquí iría la lógica para guardar la imagen
            # Por ejemplo, guardarla en un sistema de archivos o en la base de datos
            pass
            
        return {
            "message": "Usuario registrado exitosamente",
            "user": user
        }
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
  

@router.get("/{email}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
