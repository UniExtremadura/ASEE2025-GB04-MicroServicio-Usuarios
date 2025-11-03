import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Usuarios API"
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/music_usuarios"
    JWT_SECRET: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
