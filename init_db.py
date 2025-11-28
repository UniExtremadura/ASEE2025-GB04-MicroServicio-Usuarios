from app.core.database import Base, engine

from app.models import usuario_model, artista_model

print("🧨 Borrando todas las tablas...")
Base.metadata.drop_all(bind=engine)
print("✅ Tablas eliminadas.")

print("🧱 Creando nuevas tablas...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente.")

print("🚀 Inicialización de la base de datos completada.")
