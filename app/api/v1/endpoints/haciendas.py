from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.hacienda import HaciendaBasicOut, HaciendaLoteBasicOut
from app.services import hacienda_service
from app.core.errors import BusinessRuleError, business_error_to_http


router = APIRouter(prefix="/haciendas", tags=["Haciendas"])


@router.get("", response_model=list[HaciendaBasicOut])
def list_haciendas(
    productor_id: int | None = None,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    return hacienda_service.list_haciendas(
        db=db,
        actor_user=actor_user,
        productor_id=productor_id,
    )


@router.get("/{hacienda_id}/lotes", response_model=list[HaciendaLoteBasicOut])
def list_lotes(
    hacienda_id: int,
    db: Session = Depends(get_db),
    actor_user: User = Depends(get_current_user),
):
    try:
        return hacienda_service.list_lotes(
            db=db,
            actor_user=actor_user,
            hacienda_id=hacienda_id,
        )
    except BusinessRuleError as e:
        raise business_error_to_http(e)
