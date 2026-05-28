from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin
from sqlalchemy import Boolean

from app.db.base import Base
from app.models.enum import UserRole


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100))
    identificacion: Mapped[str | None] = mapped_column(String(50), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole), #
        nullable=False,
        default=UserRole.evaluador,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    #created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    #updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    empresa = relationship("Empresa", back_populates="users")

    history_events = relationship("ReporteRevision", back_populates="actor")
