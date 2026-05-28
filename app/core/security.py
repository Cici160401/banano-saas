# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any
import secrets

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def _now() -> datetime:
    return datetime.now(timezone.utc)

def _encode(payload: dict[str, Any]) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

def create_access_token(*, user_id: int, extra: dict[str, Any] | None = None) -> tuple[str, datetime]:
    exp = _now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "type": "access",
        "exp": exp,
    }
    if extra:
        payload.update(extra)
    return _encode(payload), exp

def create_refresh_token(*, user_id: int, jti: str | None = None) -> tuple[str, str, datetime]:
    # jti: token id único (para poder revocar/rotar)
    if jti is None:
        jti = secrets.token_urlsafe(32)

    exp = _now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": jti,
        "exp": exp,
    }
    return _encode(payload), jti, exp