from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.terminado_lote_marca import TerminadoLoteMarca
from app.models.terminado_lotes import TerminadoLote
from app.models.terminado_proceso_detalle import TerminadoProcesoDetalle
from app.schemas.terminado import ReporteTerminadoSave


def upsert_detalle(db: Session, reporte_id: int, detalle_in) -> TerminadoProcesoDetalle | None:
    detalle = (
        db.query(TerminadoProcesoDetalle)
        .filter(TerminadoProcesoDetalle.reporte_id == reporte_id)
        .one_or_none()
    )

    if detalle_in is None:
        return detalle

    if detalle is None:
        detalle = TerminadoProcesoDetalle(reporte_id=reporte_id)
        db.add(detalle)

    data = detalle_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(detalle, key, value)

    db.flush()
    return detalle


def replace_lotes(
    db: Session,
    detalle: TerminadoProcesoDetalle | None,
    lotes_in,
) -> list[TerminadoLote]:
    if detalle is None:
        return []

    lote_ids = [
        row.id
        for row in db.query(TerminadoLote.id)
        .filter(TerminadoLote.terminado_detalle_id == detalle.id)
        .all()
    ]

    if lote_ids:
        db.query(TerminadoLoteMarca).filter(
            TerminadoLoteMarca.lote_id.in_(lote_ids)
        ).delete(synchronize_session=False)
        db.query(TerminadoLote).filter(
            TerminadoLote.id.in_(lote_ids)
        ).delete(synchronize_session=False)

    created: list[TerminadoLote] = []
    for lote_in in lotes_in:
        lote = TerminadoLote(
            terminado_detalle_id=detalle.id,
            numero_lote=lote_in.numero_lote,
        )
        db.add(lote)
        db.flush()

        for marca_in in lote_in.marcas:
            db.add(
                TerminadoLoteMarca(
                    lote_id=lote.id,
                    marca=marca_in.marca,
                    cajas=marca_in.cajas,
                )
            )

        created.append(lote)

    db.flush()
    return created


def save_terminado_raw(
    db: Session,
    reporte_id: int,
    payload: ReporteTerminadoSave,
) -> tuple[TerminadoProcesoDetalle | None, list[TerminadoLote]]:
    detalle = upsert_detalle(db, reporte_id, payload.detalle)
    lotes = replace_lotes(db, detalle, payload.lotes)
    return detalle, lotes
