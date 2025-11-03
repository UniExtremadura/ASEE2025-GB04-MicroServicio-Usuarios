from fastapi import FastAPI
from app.routes import usuario_routes

app = FastAPI(title="Usuarios API")

# Registrar las rutas
app.include_router(usuario_routes.router, prefix="/usuarios", tags=["usuarios"])

@app.get("/")
def root():
    return {"message": "Microservicio de Usuarios activo 🚀"}
