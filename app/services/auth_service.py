# app/services/auth_service.py
from datetime import datetime, timezone
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    hash_password,  # por si lo necesitas en registro
    decode_token,
    create_access_token,
    create_refresh_token,
)
from app.models.user import User
from app.crud import refresh_token as rt_crud

class AuthError(Exception):
    pass

def _now():
    return datetime.now(timezone.utc)

def login(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise AuthError("Credenciales inválidas")
    if not user.is_active:
        raise AuthError("Usuario inactivo")

    access_token, access_exp = create_access_token(user_id=user.id)
    refresh_token, jti, refresh_exp = create_refresh_token(user_id=user.id)

    # guarda refresh en DB (hash simple: puedes usar passlib o sha256)
    token_hash = hash_password(refresh_token)  # reutilizamos bcrypt (suficiente)
    rt_crud.create_refresh_token_record(
        db,
        user_id=user.id,
        jti=jti,
        token_hash=token_hash,
        created_at=_now(),
        expires_at=refresh_exp,
    )

    db.commit()
    return {
        "access_token": access_token,
        "access_expires_at": access_exp,
        "refresh_token": refresh_token,
        "refresh_expires_at": refresh_exp,
    }

def refresh(db: Session, refresh_token: str) -> dict:
    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise AuthError("Refresh token inválido o expirado")

    if payload.get("type") != "refresh":
        raise AuthError("Token incorrecto (no es refresh)")

    sub = payload.get("sub")
    jti = payload.get("jti")
    if not sub or not jti:
        raise AuthError("Refresh token malformado")

    user_id = int(sub)

    # 1) buscar record
    rec = rt_crud.get_by_jti(db, jti)
    if not rec:
        # posible token robado o ya rotado
        raise AuthError("Refresh token no reconocido")

    if rec.revoked_at is not None:
        raise AuthError("Refresh token revocado")

    # (opcional) comparar hash del token (para evitar usar solo jti)
    # si alguien adivina jti (poco probable) no le sirve sin el token real
    from app.core.security import verify_password as _verify
    if not _verify(refresh_token, rec.token_hash):
        raise AuthError("Refresh token no coincide (posible reuse)")

    # 2) ROTACIÓN: revocar el viejo
    rt_crud.revoke(db, rec, _now())

    # 3) crear nuevos tokens
    access_token, access_exp = create_access_token(user_id=user_id)
    new_refresh_token, new_jti, new_refresh_exp = create_refresh_token(user_id=user_id)

    rt_crud.create_refresh_token_record(
        db,
        user_id=user_id,
        jti=new_jti,
        token_hash=hash_password(new_refresh_token),
        created_at=_now(),
        expires_at=new_refresh_exp,
    )

    db.commit()
    return {
        "access_token": access_token,
        "access_expires_at": access_exp,
        "refresh_token": new_refresh_token,
        "refresh_expires_at": new_refresh_exp,
    }

def logout(db: Session, refresh_token: str) -> None:
    # logout = revocar el refresh actual
    try:
        payload = decode_token(refresh_token)
    except JWTError:
        return

    if payload.get("type") != "refresh":
        return

    jti = payload.get("jti")
    if not jti:
        return

    rec = rt_crud.get_by_jti(db, jti)
    if rec and rec.revoked_at is None:
        rt_crud.revoke(db, rec, _now())
        db.commit()
