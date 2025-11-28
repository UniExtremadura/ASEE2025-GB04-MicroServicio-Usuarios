from sqlalchemy import Column, String
from app.core.database import Base

class Artist(Base):
    __tablename__ = "artists"

    email = Column(String(120), primary_key=True, unique=True, index=True)
    password = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=False) 
    avatar_url = Column(String(255), nullable=True)