from sqlalchemy import Column, String, Integer, Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    # El correo actúa como identificador único
    email = Column(String(120), primary_key=True, unique=True, index=True)
    password = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    age = Column(Integer, nullable=True)
    is_admin = Column(Boolean, default=False)
