import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from typing import Optional

# Directorio donde se guardarán las imágenes
UPLOAD_DIR = Path("uploads/avatars")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def init_upload_dir():
    """Crea el directorio de uploads si no existe"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Directorio de uploads: {UPLOAD_DIR.absolute()}")

def validate_image(file: UploadFile) -> bool:
    """Valida que el archivo sea una imagen válida"""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
    
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Extensión no permitida. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return True

async def save_avatar(file: UploadFile, user_email: str) -> str:
    """
    Guarda la imagen de perfil y retorna la URL relativa
    """
    if not file:
        return None
    
    validate_image(file)
    init_upload_dir()
    
    # Generar nombre único para evitar colisiones
    extension = file.filename.split(".")[-1].lower()
    unique_filename = f"{user_email.replace('@', '_').replace('.', '_')}_{uuid.uuid4().hex[:8]}.{extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Guardar archivo
    try:
        content = await file.read()
        
        # Validar tamaño
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="El archivo es demasiado grande (máx 5MB)")
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        print(f"✅ Imagen guardada en: {file_path.absolute()}")
        
        # Retornar URL relativa
        return f"/uploads/avatars/{unique_filename}"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar imagen: {str(e)}")

def delete_avatar(avatar_url: Optional[str]):
    """Elimina una imagen de perfil del sistema de archivos"""
    if not avatar_url:
        return
    
    try:
        filename = avatar_url.split("/")[-1]
        file_path = UPLOAD_DIR / filename
        
        if file_path.exists():
            file_path.unlink()
            print(f"✅ Avatar eliminado: {file_path}")
    except Exception as e:
        print(f"❌ Error al eliminar avatar: {str(e)}")