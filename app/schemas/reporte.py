from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Literal
from app.schemas.common import ORMBase
from app.models.enum import ReportType, ReportStatus
from app.schemas.gancho import GanchoDetalleOut, GanchoCintaOut, GanchoMotivoOut
from app.schemas.empresa import EmpresaBasicOut
from app.schemas.productor import ProductorBasicOut
from app.schemas.hacienda import HaciendaBasicOut
from app.schemas.terminado import TerminadoDetalleOut
from app.schemas.user import UserBasicOut

class ReporteBaseFields(BaseModel):
    empresa_id: int
    hacienda_id: int | None
    productor_id: int | None
    tipo: ReportType    

    semana_reporte: int | None = Field(default=None, ge=1, le=53)
    fecha_reporte: date | None

class ReporteCreateDraft(ReporteBaseFields):
    # el evaluador crea borrador (no obligamos semana/fecha todavía)
    pass

class ReporteUpdateDraft(BaseModel):
    # SOLO lo editable en borrador
    productor_id: int | None = None
    hacienda_id: int | None = None    
    semana_reporte: int | None = Field(default=None, ge=1, le=53)
    fecha_reporte: date | None = None

class ReporteSubmit(BaseModel):
    # al enviar, normalmente ya debe existir semana/fecha (validaremos en servicio)
    pass

#ESTE ES EL SCHEMA DE LO QUE SE MUESTRA CUANDO SE LLAMA A UN REPORTE REVISION (TABLA DE LA BD, es como un historial de las revisiones)
class ReporteRevisionOut(ORMBase):
    id: int
    actor: UserBasicOut
    from_status: ReportStatus
    to_status: ReportStatus
    comentario: str | None = None
    created_at: datetime

#ESTE ES EL SCHEMA DE LO QUE SE MUESTRA CUANDO SE LLAMA A UN REPORTE
class ReporteOut(ORMBase):
    id: int
    empresa_id: int
    hacienda_id: int | None
    productor_id: int | None
    created_by_user_id: int    

    tipo: ReportType
    estado: ReportStatus

    supervisor_id: int | None
    submitted_at: datetime | None
    semana_reporte: int | None
    fecha_reporte: date | None

#ESTE ES EL SCHEMA DE LO QUE SE MUESTRA CUANDO SE LLAMA A UN REPORTE, se le añaden los demas "detalles", como el gancho, las cintas
# y los motivos, y por ultimo las revisiones por las que ha pasado.
class ReporteFullOut(ReporteOut):
    empresa: EmpresaBasicOut | None = None
    productor: ProductorBasicOut | None = None
    hacienda: HaciendaBasicOut | None = None
    created_by: UserBasicOut | None = None
    supervisor: UserBasicOut | None = None
    gancho_detalle: GanchoDetalleOut | None = None
    gancho_cintas: list[GanchoCintaOut] = []
    gancho_motivos: list[GanchoMotivoOut] = []
    terminado_detalle: TerminadoDetalleOut | None = None
    historial: list[ReporteRevisionOut] = []


ReporteConGanchoOut = ReporteFullOut

class ReporteDetailOut(ORMBase):
    id: int
    tipo: ReportType
    estado: ReportStatus
    submitted_at: datetime | None
    semana_reporte: int | None
    fecha_reporte: date | None

    empresa: EmpresaBasicOut | None = None
    productor: ProductorBasicOut | None = None
    hacienda: HaciendaBasicOut | None = None
    created_by: UserBasicOut | None = None
    supervisor: UserBasicOut | None = None

    gancho_detalle: GanchoDetalleOut | None = None
    gancho_cintas: list[GanchoCintaOut] = []
    gancho_motivos: list[GanchoMotivoOut] = []
    terminado_detalle: TerminadoDetalleOut | None = None
    historial: list[ReporteRevisionOut] = []
    allowed_actions: list[str] = []

#schema de listado para usarlos en consultas de reportes con filtros
class ReporteListItemOut(ORMBase):
    id: int
    tipo: ReportType
    estado: ReportStatus
    semana_reporte: int | None
    fecha_reporte: date | None
    submitted_at: datetime | None

    productor: ProductorBasicOut | None = None
    hacienda: HaciendaBasicOut | None = None
    created_by: UserBasicOut | None = None

#schema de respuesta para la busqueda con filtros y para evitar 
class ReporteListResponse(ORMBase):
    total: int
    limit: int
    offset: int
    items: list[ReporteListItemOut]


#ESTE ES EL SCHEMA PARA GUARDAR EL REPORTE REVIEW
class ReporteReview(BaseModel):
    accion: Literal["aprobado", "rechazado"]
    comentario: str | None = None


class ReporteReopen(BaseModel):
    comentario: str = Field(..., min_length=1)
    
