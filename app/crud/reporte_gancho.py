from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.reporte_gancho_detalle import ReporteGanchoDetalle
from app.models.reporte_gancho_cinta import ReporteGanchoCinta
from app.models.reporte_gancho_motivos import ReporteGanchoMotivo
from app.schemas.gancho import ReporteGanchoSave


def upsert_detalle(db: Session, reporte_id: int, detalle_in) -> ReporteGanchoDetalle | None:
    detalle = (
        db.query(ReporteGanchoDetalle)
        .filter(ReporteGanchoDetalle.reporte_id == reporte_id)
        .one_or_none()
    )

    if detalle_in is None:
        return detalle

    if detalle is None:
        detalle = ReporteGanchoDetalle(reporte_id=reporte_id)
        db.add(detalle)

    data = detalle_in.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(detalle, k, v)

    db.flush()
    return detalle


def replace_cintas(db: Session, reporte_id: int, cintas_in) -> list[ReporteGanchoCinta]:
    db.query(ReporteGanchoCinta).filter(
        ReporteGanchoCinta.reporte_id == reporte_id
    ).delete(synchronize_session=False)

    created: list[ReporteGanchoCinta] = []
    for c in cintas_in:
        obj = ReporteGanchoCinta(
            reporte_id=reporte_id,
            semanas=c.semanas,
            descripcion=c.descripcion,
            color_id=c.color_id,
            cantidad=c.cantidad,
            porcentaje=None,
        )
        db.add(obj)
        created.append(obj)

    db.flush()
    return created


def replace_motivos(db: Session, reporte_id: int, motivos_in) -> None:
    db.query(ReporteGanchoMotivo).filter(
        ReporteGanchoMotivo.reporte_id == reporte_id
    ).delete(synchronize_session=False)

    for m in motivos_in:
        db.add(
            ReporteGanchoMotivo(
                reporte_id=reporte_id,
                motivo_id=m.motivo_id,
                cantidad=m.cantidad,
            )
        )


def save_gancho_raw(
    db: Session, reporte_id: int, payload: ReporteGanchoSave
) -> tuple[ReporteGanchoDetalle | None, list[ReporteGanchoCinta]]:
    detalle = upsert_detalle(db, reporte_id, payload.detalle)
    cintas = replace_cintas(db, reporte_id, payload.cintas)
    replace_motivos(db, reporte_id, payload.motivos)
    return detalle, cintas