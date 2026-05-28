from sqlalchemy import Integer, String, Text, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin

from app.db.base import Base
from app.models.enum import ReportStatus


class ReporteRevision(Base,TimestampMixin):
    __tablename__ = "reporte_revisiones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    reporte_id: Mapped[int] = mapped_column(ForeignKey("reportes.id"), nullable=False)
    actor_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    from_status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), nullable=False)
    to_status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), nullable=False)

    comentario: Mapped[str | None] = mapped_column(Text, nullable=True)  # por qué rechazó / qué cambiar
    snapshot: Mapped[str | None] = mapped_column(Text, nullable=True)   # opcional: JSON string futuro

    #created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    reporte = relationship("Reporte", back_populates="historial")
    actor = relationship("User", back_populates="history_events" ) 
