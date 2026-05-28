from pydantic import BaseModel, Field
from datetime import time
from app.schemas.common import ORMBase

class TerminadoDetalleIn(BaseModel):
    exportadora: str | None = None
    camion: str | None = None
    vapor: str | None = None
    puerto_acopio: str | None = None
    codigo: str | None = None

    total_cajas: int | None = Field(default=None, ge=0)
    cupo_completo: int | None = Field(default=None, ge=0)

    sello_plastico: str | None = None
    placa: str | None = None

    chofer_nombre: str | None = None
    chofer_ci: str | None = None
    chofer_telefono: str | None = None

    evaluador_nombre_texto: str | None = None
    evaluador_ci: str | None = None
    calificador_nombre: str | None = None
    hora_termino: time | None = None
    observaciones: str | None = None


class TerminadoLoteMarcaIn(BaseModel):
    marca_id: int | None = None
    marca: str | None = Field(default=None, min_length=1, max_length=150)
    cajas: int = Field(default=0, ge=0)


class TerminadoLoteIn(BaseModel):
    numero_lote: int = Field(..., ge=1)
    marcas: list[TerminadoLoteMarcaIn] = []


class ReporteTerminadoSave(BaseModel):
    detalle: TerminadoDetalleIn | None = None
    lotes: list[TerminadoLoteIn] = []


# -------- Outputs (lo que devuelves) --------

class TerminadoDetalleOut(ORMBase):
    id: int
    reporte_id: int

    exportadora: str | None
    camion: str | None
    vapor: str | None
    puerto_acopio: str | None
    codigo: str | None

    total_cajas: int | None
    cupo_completo: int | None

    sello_plastico: str | None
    placa: str | None

    chofer_nombre: str | None
    chofer_ci: str | None
    chofer_telefono: str | None

    evaluador_nombre_texto: str | None
    evaluador_ci: str | None
    calificador_nombre: str | None
    hora_termino: time | None
    observaciones: str | None
    lotes: list["TerminadoLoteOut"] = []


class TerminadoLoteMarcaOut(ORMBase):
    id: int
    lote_id: int
    marca: str
    cajas: int


class TerminadoLoteOut(ORMBase):
    id: int
    terminado_detalle_id: int
    numero_lote: int
    marcas: list[TerminadoLoteMarcaOut] = []
