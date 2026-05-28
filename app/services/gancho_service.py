from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.reporte import Reporte
from app.models.enum import ReportStatus, ReportType
from app.models.reporte_gancho_cinta import ReporteGanchoCinta
from app.schemas.gancho import ReporteGanchoSave
from app.crud import reporte_gancho as gancho_crud
from app.core.permissions import can_create_or_edit_reporte
from app.core.errors import BusinessRuleError


def ensure_reporte_is_gancho(reporte: Reporte) -> None:
    if reporte.tipo != ReportType.reporte_de_gancho:
        raise BusinessRuleError("Este reporte no es de tipo GANCHO.")


def ensure_reporte_editable(reporte: Reporte) -> None:
    if reporte.estado not in (ReportStatus.draft, ReportStatus.needs_changes):
        raise BusinessRuleError("Este reporte ya no se puede editar.", 403)

def ensure_can_edit_gancho(actor_user: User, reporte: Reporte) -> None:
    if not can_create_or_edit_reporte(actor_user, reporte):
        raise BusinessRuleError("No tienes permiso para editar.", 403)

def q(value: Decimal, pattern: str) -> Decimal:
    return value.quantize(Decimal(pattern), rounding=ROUND_HALF_UP)


def calc_ratio(cupo_total: int | None, racimos_procesados: int | None) -> Decimal | None:
    # ratio = cupo_total / racimos_procesados
    if cupo_total is None or racimos_procesados is None or racimos_procesados <= 0:
        return None
    return q(Decimal(cupo_total) / Decimal(racimos_procesados), "0.0001")


def calc_porcentaje(cantidad: int | None, racimos_procesados: int | None) -> Decimal | None:
    # porcentaje = cantidad / racimos_procesados * 100  (como tus ejemplos)
    if cantidad is None or racimos_procesados is None or racimos_procesados <= 0:
        return None
    return q((Decimal(cantidad) / Decimal(racimos_procesados)) * Decimal(100), "0.01")


def save_gancho(db: Session, actor_user: User, reporte: Reporte, payload: ReporteGanchoSave) -> Reporte:
    ensure_can_edit_gancho(actor_user, reporte)
    ensure_reporte_is_gancho(reporte)
    ensure_reporte_editable(reporte)

    detalle, cintas_db = gancho_crud.save_gancho_raw(db, reporte.id, payload)

    if detalle is not None:
        detalle.ratio = calc_ratio(detalle.cupo_total, detalle.racimos_procesados)

    racimos_procesados = detalle.racimos_procesados if detalle else None

    for c in cintas_db:
        c.porcentaje = calc_porcentaje(c.cantidad, racimos_procesados)

    db.commit()
    db.refresh(reporte)
    return reporte
