from pydantic import BaseModel
from typing import Optional

class ArtistCreate(BaseModel):
    email: str
    password: str
    display_name: str
    avatar_url: Optional[str] = None  

class ArtistUpdate(BaseModel):
    display_name: Optional[str] = None 
    password: Optional[str] = None
    avatar_url: Optional[str] = None

class ArtistResponse(BaseModel):
    email: str
    display_name: Optional[str] = None 
    avatar_url: Optional[str] = None  

    class Config:
        from_attributes = True