from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UserCreate, UserResponse
from app.services.usuario_service import register_user, get_user_by_email, get_password_hash 
from app.services.image_service import save_avatar
from app.core.database import get_db
from app.dao.usuario_dao import update_user, get_user_by_email as dao_get_user

router = APIRouter()
    
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
        # 👇 Primero guardar la imagen si existe
        avatar_url = None
        if img_perfil:
            avatar_url = await save_avatar(img_perfil, email)
        
        # 👇 Crear el usuario CON la URL del avatar
        user_data = UserCreate(
            email=email,
            password=password,
            display_name=nombre_completo,
            full_name=nombre_completo,
            age=edad,
            avatar_url=avatar_url  
        )
        
        # Registrar el usuario 
        user = register_user(user_data, db)
            
        return {
            "message": "Usuario registrado exitosamente",
            "user": user
        }
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{email}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def actualizar_perfil(
    email: str,
    display_name: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Actualiza el perfil de un usuario.
    
    - **email**: Email del usuario (path parameter)
    - **display_name**: Nuevo nombre de usuario (opcional)
    - **password**: Nueva contraseña (opcional)
    - **avatar**: Nueva imagen de perfil (opcional)
    """
    # Verificar que el usuario existe
    db_user = dao_get_user(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    try:
        update_data = {}
        
        # Actualizar display_name si se proporciona
        if display_name:
            update_data["display_name"] = display_name
        
        # Actualizar password si se proporciona
        if password:
            update_data["password"] = get_password_hash(password)  
        
        # Actualizar avatar si se proporciona
        if avatar:
            old_avatar_url = db_user.avatar_url
            new_avatar_url = await save_avatar(avatar, email, old_avatar_url)
            update_data["avatar_url"] = new_avatar_url
        
        # Si no hay nada que actualizar
        if not update_data:
            raise HTTPException(
                status_code=400, 
                detail="Debe proporcionar al menos un campo para actualizar"
            )
        
        # Actualizar usuario en la BD
        updated_user = update_user(db, email, **update_data)
        
        return updated_user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar usuario: {str(e)}")


@router.get("/{email}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
