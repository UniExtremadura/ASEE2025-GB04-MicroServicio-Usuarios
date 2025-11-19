from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import usuario_routes, artista_routes, auth_routes 
from app.services.image_service import init_upload_dir
import os

app = FastAPI(title="Usuarios API")

# Inicializar directorio de uploads
init_upload_dir()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (DESPUÉS de CORS)
# Verificar que el directorio existe
if os.path.exists("uploads"):
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
else:
    print("⚠️ Advertencia: No existe el directorio 'uploads'")

# Registrar las rutas
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"]) 
app.include_router(usuario_routes.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(artista_routes.router, prefix="/artistas", tags=["artistas"])

@app.get("/")
def root():
    return {"message": "Microservicio de Usuarios activo 🚀"}
