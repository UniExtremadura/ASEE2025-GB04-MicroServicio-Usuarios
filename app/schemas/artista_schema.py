from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional

class ArtistCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: str
    avatar_url: Optional[HttpUrl] = None


class ArtistResponse(BaseModel):
    email: EmailStr
    display_name: str
    avatar_url: Optional[HttpUrl] = None

    model_config = {"from_attributes": True}
