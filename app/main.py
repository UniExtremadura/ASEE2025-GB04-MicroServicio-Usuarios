from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import usuario_routes, artista_routes
from app.services.image_service import init_upload_dir
import os

app = FastAPI(title="Usuarios API")

# Inicializar directorio de uploads
init_upload_dir()

# Configuración de CORS (ANTES de montar static files)
origins = [
        "http://localhost:5501",    # VS Code Live Server default
        "http://127.0.0.1:5501",    # VS Code Live Server alternative
        "http://127.0.0.1:8000",    # FastAPI default
        "http://localhost:5173",     # Vite default
        "http://127.0.0.1:5173",     # Vite alternative
    # Añade aquí otros orígenes permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
app.include_router(usuario_routes.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(artista_routes.router, prefix="/artistas", tags=["artistas"])

@app.get("/")
def root():
    return {"message": "Microservicio de Usuarios activo 🚀"}
