from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    display_name: str
    avatar_url: Optional[HttpUrl] = None
    age: Optional[int] = None
    is_admin: bool = False

class UserCreate(BaseModel):
    email: str
    password: str
    display_name: str
    full_name: str
    age: Optional[int] = None
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    email: str
    display_name: str
    full_name: str
    avatar_url: Optional[str] = None  # 👈 Añadir este campo
    age: Optional[int] = None
    is_admin: bool = False

    class Config:
        from_attributes = True
