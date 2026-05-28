# app/schemas/gancho.py
from pydantic import BaseModel, Field
from decimal import Decimal
from app.schemas.common import ORMBase


class GanchoDetalleIn(BaseModel):
    cupo_total: int | None = None
    racimos_cosechados: int | None = None
    racimos_procesados: int | None = None
    racimos_rechazados: int | None = None
    observaciones: str | None = None

class GanchoCintaIn(BaseModel):
    semanas: int | None = None
    descripcion: str | None = None
    color_id: int  # viene del catálogo por empresa
    cantidad: int | None = None
    #porcentaje: Decimal | None = Field(default=None, max_digits=6, decimal_places=2)

class GanchoMotivoIn(BaseModel):
    motivo_id: int
    cantidad: int | None = None


## ESTOS SON LOS SCHEMAS PARA MOSTRAR en el GANCHO OUT
class ColorOut(ORMBase):
    id: int
    nombre: str
    hex: str | None = None
## ESTOS SON LOS SCHEMAS PARA MOSTRAR en el GANCHO OUT
class MotivoOut(ORMBase):
    id: int
    nombre: str
########

class ReporteGanchoSave(BaseModel):
    detalle: GanchoDetalleIn | None
    cintas: list[GanchoCintaIn] = []
    motivos: list[GanchoMotivoIn] = []

class GanchoDetalleOut(ORMBase):
    id: int
    cupo_total: int | None
    racimos_cosechados: int | None
    racimos_procesados: int | None
    racimos_rechazados: int | None
    ratio: Decimal | None
    observaciones: str | None
    
class GanchoCintaOut(ORMBase):
    id: int
    semanas: int | None
    descripcion: str | None
    color: ColorOut | None = None
    cantidad: int | None
    porcentaje: Decimal | None

class GanchoMotivoOut(ORMBase):
    id: int
    motivo: MotivoOut | None = None
    cantidad: int | None