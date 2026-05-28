# app/api/v1/endpoints/catalogos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.cinta_color import CintaColorBasicOut
from app.schemas.marca import MarcaBasicOut
from app.schemas.motivos import MotivoGanchoBasicOut

from app.services import cinta_color_service, marca_service, motivo_service

router = APIRouter(prefix="/catalogos", tags=["Catalogos"])

@router.get("/colores", response_model=list[CintaColorBasicOut])
def list_colores(
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    return cinta_color_service.list_color(db=db, actor_user=actor_user)

@router.get("/motivos", response_model=list[MotivoGanchoBasicOut])
def list_motivos(
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    return motivo_service.list_motivos(db=db, actor_user=actor_user)


@router.get("/marcas", response_model=list[MarcaBasicOut])
def list_marcas(
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    return marca_service.list_marcas(db=db, actor_user=actor_user)
