# app/api/v1/endpoints/gancho.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.reporte import Reporte

from app.schemas.gancho import ReporteGanchoSave
from app.schemas.reporte import ReporteOut

from app.services import gancho_service
from app.core.errors import BusinessRuleError, business_error_to_http

router = APIRouter(prefix="/reportes", tags=["Gancho"])


def get_reporte_or_404(db: Session, reporte_id: int) -> Reporte:
    obj = db.get(Reporte, reporte_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Reporte no existe")
    return obj


@router.put(
    "/{reporte_id}/gancho",
    response_model=ReporteOut,
)
def save_gancho(
    reporte_id: int,
    payload: ReporteGanchoSave,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    reporte = get_reporte_or_404(db, reporte_id)

    try:
        return gancho_service.save_gancho(db, actor_user, reporte, payload)
    except BusinessRuleError as e:
        raise business_error_to_http(e)
