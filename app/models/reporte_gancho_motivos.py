from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin
from app.db.base import Base


class ReporteGanchoMotivo(Base,TimestampMixin):
    __tablename__ = "reporte_gancho_motivos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reporte_id: Mapped[int] = mapped_column(ForeignKey("reportes.id"), nullable=False)

    motivo_id: Mapped[int] = mapped_column(ForeignKey("motivos_gancho.id"), nullable=False)
    cantidad: Mapped[int | None] = mapped_column(Integer, nullable=True)

    reporte = relationship("Reporte", back_populates="gancho_motivos")
    motivo = relationship("MotivoGancho", back_populates="reporte_motivos")
