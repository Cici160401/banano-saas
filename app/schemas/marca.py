from datetime import datetime

from app.schemas.common import ORMBase


class MarcaOut(ORMBase):
    id: int
    empresa_id: int
    nombre: str
    activo: int
    orden: int
    created_at: datetime
    updated_at: datetime


class MarcaBasicOut(ORMBase):
    id: int
    nombre: str
