from sqlalchemy.orm import Session

from app.crud import marcas as marcas_crud
from app.models.marca import Marca
from app.models.user import User


def list_marcas(db: Session, actor_user: User) -> list[Marca]:
    return marcas_crud.list_marcas(db=db, empresa_id=actor_user.empresa_id)
