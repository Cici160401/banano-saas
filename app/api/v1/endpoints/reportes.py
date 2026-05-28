from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth import get_current_user  # ajusta a tu proyecto
from app.models.user import User
from app.models.reporte import Reporte
from app.schemas.reporte import ReporteListResponse
from app.models.enum import ReportType, ReportStatus
from datetime import date

from app.schemas.reporte import (
    ReporteCreateDraft,
    ReporteUpdateDraft,
    ReporteOut,
    ReporteFullOut,
    ReporteReopen,
    ReporteReview,
    ReporteDetailOut
)
from app.services import reporte_service
from app.core.errors import BusinessRuleError, business_error_to_http

router = APIRouter(prefix="/reportes", tags=["Reportes"])


def get_reporte_or_404(db: Session, reporte_id: int) -> Reporte:
    obj = db.get(Reporte, reporte_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Reporte no existe")
    return obj


@router.post("/drafts",response_model=ReporteOut,status_code=status.HTTP_201_CREATED,)
def create_reporte_draft(
    payload: ReporteCreateDraft,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    try:
        return reporte_service.create_draft(db, payload, actor_user)
    except BusinessRuleError as e:
        raise business_error_to_http(e)


@router.get("/{reporte_id}",response_model=ReporteDetailOut,)
def get_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    try:
        return reporte_service.get_reporte_detail(db, reporte_id, actor_user)
    except BusinessRuleError as e:
        raise business_error_to_http(e)

#ESTE ES EL ENDPOINT PARA EDITAR EL DRAFT Y AÑADIRLE LA PARTE DE GANCHO DETALLE
@router.patch("/{reporte_id}/draft",response_model=ReporteOut,)
def update_reporte_draft(
    reporte_id: int,
    patch: ReporteUpdateDraft,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    reporte = get_reporte_or_404(db, reporte_id)
    try:
        return reporte_service.update_draft(db, reporte, patch, actor_user)
    except BusinessRuleError as e:
        raise business_error_to_http(e)


@router.post("/{reporte_id}/submit",response_model=ReporteOut,)
def submit_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    reporte = get_reporte_or_404(db, reporte_id)
    try:
        return reporte_service.submit_reporte(db, reporte, actor_user)
    except BusinessRuleError as e:
        raise business_error_to_http(e)
    

@router.post("/{reporte_id}/review", response_model=ReporteFullOut)
def review_reporte(
    reporte_id: int,
    payload: ReporteReview,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    reporte = get_reporte_or_404(db, reporte_id)

    try:
        return reporte_service.review_reporte(db, reporte, payload, actor_user)
    except BusinessRuleError as e:
        raise business_error_to_http(e)
    
@router.get("", response_model=ReporteListResponse)
def list_reportes(
    estado: ReportStatus | None = None,
    tipo: ReportType | None = None,
    semana_reporte: int | None = None,
    productor_id: int | None = None,
    hacienda_id: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
    search: str | None = None,
    order_by: str | None = None,
    order_dir: str | None = "desc",
):
    try:
        return reporte_service.list_reportes(
        db=db,
        actor_user=actor_user,
        estado=estado,
        tipo=tipo,
        semana_reporte=semana_reporte,
        productor_id=productor_id,
        hacienda_id=hacienda_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limit=limit,
        offset=offset,
        search=search,
        order_by=order_by,
        order_dir=order_dir
    )
    except BusinessRuleError as e:
        raise business_error_to_http(e)

@router.post("/{reporte_id}/start-review", response_model=ReporteOut)
def start_review(
    reporte_id: int,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    reporte = get_reporte_or_404(db, reporte_id)

    try:
        return reporte_service.start_review(db, reporte, actor_user)
    except BusinessRuleError as e:
        raise business_error_to_http(e)


@router.post("/{reporte_id}/reopen", response_model=ReporteOut)
def reopen_reporte(
    reporte_id: int,
    payload: ReporteReopen,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    reporte = get_reporte_or_404(db, reporte_id)

    try:
        return reporte_service.reopen_reporte(db, reporte, payload, actor_user)
    except BusinessRuleError as e:
        raise business_error_to_http(e)
