from sqlalchemy.orm import Session
from app.models.user import User
from app.crud import cinta_color as cinta_color_crud

def list_color(db: Session, actor_user: User):
   return cinta_color_crud.list_colores(
       db=db,
       empresa_id=actor_user.empresa_id
   )
