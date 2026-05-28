# app/crud/refresh_token.py
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken

def create_refresh_token_record(
    db: Session,
    *,
    user_id: int,
    jti: str,
    token_hash: str,
    created_at: datetime,
    expires_at: datetime,
) -> RefreshToken:
    obj = RefreshToken(
        user_id=user_id,
        jti=jti,
        token_hash=token_hash,
        created_at=created_at,
        expires_at=expires_at,
        revoked_at=None,
    )
    db.add(obj)
    return obj

def get_by_jti(db: Session, jti: str) -> RefreshToken | None:
    return db.query(RefreshToken).filter(RefreshToken.jti == jti).one_or_none()

def revoke(db: Session, obj: RefreshToken, when: datetime) -> None:
    obj.revoked_at = when
    db.add(obj)