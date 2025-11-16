from pydantic import BaseModel

class LoginRequest(BaseModel):
    """Schema para login (común para usuarios y artistas)"""
    email: str
    password: str

class TokenResponse(BaseModel):
    """Respuesta del login con token"""
    access_token: str
    token_type: str
    user_type: str  # "user" o "artist"
    user_data: dict

class MeResponse(BaseModel):
    """Respuesta del endpoint /auth/me"""
    user_type: str
    user_data: dict