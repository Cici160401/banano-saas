# app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.models.user import User

# En esta clase definimos las funciones de autenticación automática que puedo usar como dependencia en mis rutas
#---Ejemplo: get_current_user --> toma el token de usuario, lo verifica y retorna el usuario si es válido.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme),) -> User:
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if not sub:
            raise unauth_exc
        user_id = int(sub)
    except (JWTError, ValueError):
        raise unauth_exc

    user = db.get(User, user_id)
    if not user:
        raise unauth_exc
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    return user