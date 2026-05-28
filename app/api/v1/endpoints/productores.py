from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.productor import ProductorBasicOut
from app.services import productor_service


router = APIRouter(prefix="/productores", tags=["Productores"])


@router.get("", response_model=list[ProductorBasicOut])
def list_productores(
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    return productor_service.list_productores(db=db, actor_user=actor_user)
