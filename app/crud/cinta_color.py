from app.models.cinta_color import CintaColor
from app.models.user import User, UserRole
from app.models.enum import ReportStatus
from sqlalchemy.orm import Session, selectinload


def list_colores(db: Session, empresa_id: int) -> CintaColor | None:
    query = db.query(CintaColor)
    query = query.filter(CintaColor.empresa_id == empresa_id)
    query = query.filter(CintaColor.activo == 1)
    query = query.order_by(CintaColor.orden.asc(), CintaColor.id.asc())

    return query.all()



