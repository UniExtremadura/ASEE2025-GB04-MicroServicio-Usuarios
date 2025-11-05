from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import usuario_routes, artista_routes

app = FastAPI(title="Usuarios API")

# Configuración de CORS
origins = [
        "http://localhost:5501",    # VS Code Live Server default
        "http://127.0.0.1:5501",    # VS Code Live Server alternative
        "http://127.0.0.1:8000"     # FastAPI default
    # Añade aquí otros orígenes permitidos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar las rutas
app.include_router(usuario_routes.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(artista_routes.router, prefix="/artistas", tags=["artistas"])
@app.get("/")
def root():
    return {"message": "Microservicio de Usuarios activo 🚀"}
