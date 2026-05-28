# app/models/motivo_gancho.py

from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin
from app.db.base import Base


class MotivoGancho(Base, TimestampMixin):
    __tablename__ = "motivos_gancho"
    __table_args__ = (
        UniqueConstraint("empresa_id", "nombre", name="uq_motivo_gancho_empresa_nombre"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False, index=True)

    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    activo: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    orden: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    empresa = relationship("Empresa")
    reporte_motivos = relationship("ReporteGanchoMotivo", back_populates="motivo")