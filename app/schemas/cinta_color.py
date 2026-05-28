from pydantic import BaseModel
from app.schemas.common import ORMBase
from datetime import datetime

class CintaColorOut(ORMBase):
    id: int
    empresa_id: int
    nombre: str
    hex: str | None
    activo: int
    orden: int
    created_at: datetime
    updated_at: datetime

class CintaColorBasicOut(BaseModel):
    id: int
    nombre: str
    hex: str | None

    class Config:
        from_attributes = True
