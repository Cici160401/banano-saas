from app.models.motivo_gancho import MotivoGancho
from app.models.user import User, UserRole
from app.models.enum import ReportStatus
from sqlalchemy.orm import Session, selectinload


def list_motivos(db: Session, empresa_id: int) -> MotivoGancho | None:
    query = db.query(MotivoGancho)
    query = query.filter(MotivoGancho.empresa_id == empresa_id)    
    query = query.order_by(MotivoGancho.orden.asc(), MotivoGancho.id.asc())

    return query.all()
