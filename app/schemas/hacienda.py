from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

class HaciendaBaseFields(BaseModel):
    empresa_id: int
    productor_id: int
    codigo_hacienda: int
    nombre: str = Field(..., min_length=2, max_length=150)

    hectareas: float | None = Field(default=None, ge=0)
    zona: str | None = Field(default=None, max_length=120)
    lote: str | None = Field(default=None, max_length=80)
    direccion: str | None = Field(default=None, max_length=255)

class HaciendaCreate(HaciendaBaseFields):
    pass

class HaciendaUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    hectareas: float | None = Field(default=None, ge=0)
    zona: str | None = Field(default=None, max_length=120)
    lote: str | None = Field(default=None, max_length=80)
    direccion: str | None = Field(default=None, max_length=255)
    productor_id: int | None = None

class HaciendaOut(ORMBase):
    id: int
    empresa_id: int
    productor_id: int
    codigo_hacienda: int
    nombre: str
    hectareas: float | None = None
    zona: str | None = None
    lote: str | None = None
    direccion: str | None = None

class HaciendaBasicOut(ORMBase):
    id: int
    codigo_hacienda: int
    nombre: str
    zona: str | None = None


class HaciendaLoteBasicOut(ORMBase):
    id: int
    numero_lote: int
