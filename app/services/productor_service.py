from sqlalchemy.orm import Session

from app.crud import productores as productores_crud
from app.models.productor import Productor
from app.models.user import User


def list_productores(db: Session, actor_user: User) -> list[Productor]:
    return productores_crud.list_productores(
        db=db,
        empresa_id=actor_user.empresa_id,
    )
