from pydantic import BaseModel
from typing import Optional

class ArtistCreate(BaseModel):
    email: str
    password: str
    display_name: str
    avatar_url: Optional[str] = None  


class ArtistResponse(BaseModel):
    email: str
    display_name: str
    avatar_url: Optional[str] = None  

    class Config:
        from_attributes = True
