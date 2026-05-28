from __future__ import annotations

from sqlalchemy.orm import Session

from app.crud import terminado as terminado_crud
from app.models.enum import ReportStatus, ReportType
from app.models.hacienda_lote import HaciendaLote
from app.models.marca import Marca
from app.models.reporte import Reporte
from app.models.user import User
from app.schemas.terminado import ReporteTerminadoSave
from app.core.permissions import can_create_or_edit_reporte
from app.core.errors import BusinessRuleError


def ensure_reporte_is_terminado(reporte: Reporte) -> None:
    if reporte.tipo != ReportType.terminados_de_proceso:
        raise BusinessRuleError("Este reporte no es de tipo TERMINADO.")


def ensure_reporte_editable(reporte: Reporte) -> None:
    if reporte.estado not in (ReportStatus.draft, ReportStatus.needs_changes):
        raise BusinessRuleError("Este reporte ya no se puede editar.", 403)


def ensure_can_edit_terminado(actor_user: User, reporte: Reporte) -> None:
    if not can_create_or_edit_reporte(actor_user, reporte):
        raise BusinessRuleError("No tienes permiso para editar.", 403)


def resolve_marca_nombre(db: Session, empresa_id: int, marca_id: int | None, marca_texto: str | None) -> str:
    if marca_id is None and not marca_texto:
        raise BusinessRuleError("Cada marca debe tener marca_id o marca.")

    if marca_id is None:
        nombre = str(marca_texto).strip()
        if not nombre:
            raise BusinessRuleError("El nombre de la marca no puede estar vacio.")
        return nombre

    marca = (
        db.query(Marca)
        .filter(Marca.id == marca_id, Marca.empresa_id == empresa_id, Marca.activo == 1)
        .one_or_none()
    )
    if marca is None:
        raise BusinessRuleError("La marca indicada no existe o no pertenece a tu empresa.")

    return marca.nombre


def ensure_lotes_belong_to_hacienda(db: Session, reporte: Reporte, payload: ReporteTerminadoSave) -> None:
    if reporte.hacienda_id is None:
        raise BusinessRuleError("Primero selecciona una hacienda para registrar lotes.")

    numeros_lote = [lote.numero_lote for lote in payload.lotes]
    if len(numeros_lote) != len(set(numeros_lote)):
        raise BusinessRuleError("No puedes repetir el mismo lote en el terminado.")

    if not numeros_lote:
        return

    existing = {
        row.numero_lote
        for row in db.query(HaciendaLote.numero_lote)
        .filter(
            HaciendaLote.hacienda_id == reporte.hacienda_id,
            HaciendaLote.numero_lote.in_(numeros_lote),
        )
        .all()
    }
    missing = sorted(set(numeros_lote) - existing)
    if missing:
        raise BusinessRuleError(
            f"Los lotes no pertenecen a la hacienda seleccionada: {', '.join(map(str, missing))}."
        )


def normalize_payload_marcas(db: Session, reporte: Reporte, payload: ReporteTerminadoSave) -> ReporteTerminadoSave:
    normalized = payload.model_copy(deep=True)

    for lote in normalized.lotes:
        for marca in lote.marcas:
            marca.marca = resolve_marca_nombre(
                db=db,
                empresa_id=reporte.empresa_id,
                marca_id=marca.marca_id,
                marca_texto=marca.marca,
            )

    return normalized


def apply_total_cajas(payload: ReporteTerminadoSave) -> ReporteTerminadoSave:
    normalized = payload.model_copy(deep=True)

    if normalized.detalle is None:
        return normalized

    normalized.detalle.total_cajas = sum(
        marca.cajas
        for lote in normalized.lotes
        for marca in lote.marcas
        if marca.cajas is not None
    )
    return normalized


def apply_evaluador_defaults(actor_user: User, payload: ReporteTerminadoSave) -> ReporteTerminadoSave:
    normalized = payload.model_copy(deep=True)

    if normalized.detalle is None:
        return normalized

    if normalized.detalle.evaluador_nombre_texto is None:
        normalized.detalle.evaluador_nombre_texto = actor_user.nombre

    if normalized.detalle.evaluador_ci is None:
        normalized.detalle.evaluador_ci = actor_user.identificacion

    return normalized


def save_terminado(
    db: Session,
    actor_user: User,
    reporte: Reporte,
    payload: ReporteTerminadoSave,
) -> Reporte:
    ensure_can_edit_terminado(actor_user, reporte)
    ensure_reporte_is_terminado(reporte)
    ensure_reporte_editable(reporte)
    ensure_lotes_belong_to_hacienda(db, reporte, payload)

    normalized = apply_evaluador_defaults(actor_user, payload)
    normalized = normalize_payload_marcas(db, reporte, normalized)
    normalized = apply_total_cajas(normalized)
    terminado_crud.save_terminado_raw(db, reporte.id, normalized)

    db.commit()
    db.refresh(reporte)
    return reporte
