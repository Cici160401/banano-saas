from sqlalchemy.orm import Session

from app.crud import haciendas as haciendas_crud
from app.models.hacienda import Hacienda
from app.models.hacienda_lote import HaciendaLote
from app.models.user import User
from app.core.errors import BusinessRuleError


def list_haciendas(
    db: Session,
    actor_user: User,
    productor_id: int | None = None,
) -> list[Hacienda]:
    return haciendas_crud.list_haciendas(
        db=db,
        empresa_id=actor_user.empresa_id,
        productor_id=productor_id,
    )


def list_lotes(
    db: Session,
    actor_user: User,
    hacienda_id: int,
) -> list[HaciendaLote]:
    hacienda = haciendas_crud.get_hacienda_by_empresa(
        db=db,
        hacienda_id=hacienda_id,
        empresa_id=actor_user.empresa_id,
    )
    if not hacienda:
        raise BusinessRuleError("Hacienda no existe", 404)

    return haciendas_crud.list_lotes_by_hacienda(db=db, hacienda_id=hacienda_id)
