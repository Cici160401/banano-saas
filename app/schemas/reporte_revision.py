from pydantic import BaseModel
from app.schemas.common import ORMBase
from app.models.enum import ReportStatus

class ReporteRevisionBase (BaseModel):
    reporte_id: int
    actor_user_id: int
    from_status: ReportStatus
    to_status:  ReportStatus
    comentario: str
    snapshot: str

class ReporteRevisionCreate (ReporteRevisionBase):
    pass

class ReporteRevisionOut (ORMBase):
    id :int
    reporte_id: int
    actor_user_id: int
    from_status: ReportStatus
    to_status:  ReportStatus
    comentario: str | None
    snapshot: str | None
   
