from sqlalchemy.orm import Session

from app.models.productor import Productor


def list_productores(db: Session, empresa_id: int) -> list[Productor]:
    return (
        db.query(Productor)
        .filter(Productor.empresa_id == empresa_id)
        .order_by(Productor.nombre.asc(), Productor.id.asc())
        .all()
    )
