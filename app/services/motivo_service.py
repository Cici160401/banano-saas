from sqlalchemy.orm import Session
from app.models.user import User
from app.crud import motivos as motivo_crud

def list_motivos(db: Session, actor_user: User):
   return motivo_crud.list_motivos(
       db=db,
       empresa_id=actor_user.empresa_id
   )
