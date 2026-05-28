# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import auth_service
from app.schemas.auth import RefreshIn as RefreshSchema

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        return auth_service.login(db, email=form.username, password=form.password)
    except auth_service.AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))

class RefreshIn(RefreshSchema):
    refresh_token: str

@router.post("/refresh")
def refresh(payload: RefreshIn, db: Session = Depends(get_db)):
    try:
        return auth_service.refresh(db, payload.refresh_token)
    except auth_service.AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
def logout(payload: RefreshIn, db: Session = Depends(get_db)):
    auth_service.logout(db, payload.refresh_token)
    return {"ok": True}