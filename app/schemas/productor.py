from pydantic import BaseModel
from app.schemas.common import ORMBase

class ProductorCreate(BaseModel):
    codigo_productor: int
    nombre: str
    identificacion: str
    telefono: str | None = None

class ProductorUpdate(BaseModel):
    nombre: str | None = None
    identificacion: str | None = None
    telefono: str | None = None

class ProductorOut(ORMBase):
    id: int
    empresa_id: int
    codigo_productor: int
    nombre: str
    identificacion: str
    telefono: str | None

class ProductorBasicOut(ORMBase):
    id: int
    codigo_productor: int
    nombre: str
