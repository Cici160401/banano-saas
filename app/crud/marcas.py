from sqlalchemy.orm import Session

from app.models.marca import Marca


def list_marcas(db: Session, empresa_id: int) -> list[Marca]:
    return (
        db.query(Marca)
        .filter(Marca.empresa_id == empresa_id)
        .filter(Marca.activo == 1)
        .order_by(Marca.orden.asc(), Marca.nombre.asc(), Marca.id.asc())
        .all()
    )
