from sqlalchemy.orm import Session

from app.models.hacienda import Hacienda
from app.models.hacienda_lote import HaciendaLote


def list_haciendas(
    db: Session,
    empresa_id: int,
    productor_id: int | None = None,
) -> list[Hacienda]:
    query = db.query(Hacienda).filter(Hacienda.empresa_id == empresa_id)

    if productor_id is not None:
        query = query.filter(Hacienda.productor_id == productor_id)

    return query.order_by(Hacienda.nombre.asc(), Hacienda.id.asc()).all()


def get_hacienda_by_empresa(
    db: Session,
    hacienda_id: int,
    empresa_id: int,
) -> Hacienda | None:
    return (
        db.query(Hacienda)
        .filter(Hacienda.id == hacienda_id, Hacienda.empresa_id == empresa_id)
        .first()
    )


def list_lotes_by_hacienda(db: Session, hacienda_id: int) -> list[HaciendaLote]:
    return (
        db.query(HaciendaLote)
        .filter(HaciendaLote.hacienda_id == hacienda_id)
        .order_by(HaciendaLote.numero_lote.asc(), HaciendaLote.id.asc())
        .all()
    )
