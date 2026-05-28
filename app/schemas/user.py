from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.common import ORMBase
from app.models.enum import UserRole
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    nombre: str | None = Field(default=None, max_length=100)
    identificacion: str | None = Field(default=None, max_length=50)
    role: UserRole = UserRole.evaluador
    avatar_url: str | None = Field(default=None, max_length=500)
    is_active: int = 1

class UserCreate(BaseModel):
    empresa_id: int
    nombre: str | None = Field(default=None, max_length=100)
    identificacion: str | None = Field(default=None, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.evaluador
    avatar_url: str | None = None
    is_active: int = 1
    
class UserUpdate():
    email: Optional[EmailStr] = None
    avatarUrl: Optional[str] = None
    password: Optional[str] = None


class UserOut(ORMBase):
    id: int
    empresa_id: int
    nombre: str
    identificacion: str | None
    email: EmailStr
    role: UserRole
    avatar_url: str | None
    is_active: int
    created_at: datetime
    updated_at: datetime

#LO QUE EL ADMIN PUEDE CAMBIAR
class UserUpdateAdmin(BaseModel):
    # update parcial: admin puede cambiar rol/activo
    role: UserRole | None = None
    is_active: int | None = Field(default=None, ge=0, le=1)

#ESTA SALIDA LA USAREMOS PARA EL HISTORIAL DE REVISIONES
class UserBasicOut(BaseModel):
    id: int
    nombre: str
    identificacion: str | None = None

    class Config:
        from_attributes = True

# =========================
# AUTH (login)
# =========================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

