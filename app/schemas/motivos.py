from datetime import datetime
from pydantic import BaseModel
from app.schemas.common import ORMBase


class MotivoGanchoOut(ORMBase):
    id: int
    empresa_id: int
    nombre: str
    activo: int
    orden: int
    created_at: datetime
    updated_at: datetime


class MotivoGanchoBasicOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True