from sqlalchemy import Integer, DateTime, func, ForeignKey, Enum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin


from app.db.base import Base
from app.models.enum import ReportType, ReportStatus


class Reporte(Base, TimestampMixin):
    __tablename__ = "reportes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    hacienda_id: Mapped[int] = mapped_column(ForeignKey("haciendas.id"), nullable=True)
    productor_id: Mapped[int] = mapped_column(ForeignKey("productores.id"), nullable=True)
     # datos del negocio
    semana_reporte: Mapped[int | None] = mapped_column(Integer, nullable=True)      # 1..53
    fecha_reporte: Mapped[Date | None] = mapped_column(Date, nullable=True)        # día del reporte

    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    tipo: Mapped[ReportType] = mapped_column(Enum(ReportType), nullable=False)
    estado: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), nullable=False, default=ReportStatus.draft)

    # supervisor asignado (opcional)
    supervisor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    submitted_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

    #created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    #updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    empresa = relationship("Empresa")
    hacienda = relationship("Hacienda", back_populates="reportes")
    productor = relationship("Productor", back_populates="reportes")

    created_by = relationship("User", foreign_keys=[created_by_user_id])
    supervisor = relationship("User", foreign_keys=[supervisor_id])

    historial = relationship("ReporteRevision", back_populates="reporte", cascade="all, delete-orphan")

    gancho_detalle = relationship(
        "ReporteGanchoDetalle",
        back_populates="reporte",
        cascade="all, delete-orphan",
        uselist=False,
    )

    gancho_cintas = relationship(
        "ReporteGanchoCinta",
        back_populates="reporte",
        cascade="all, delete-orphan"
    )

    gancho_motivos = relationship(
        "ReporteGanchoMotivo",
        back_populates="reporte",
        cascade="all, delete-orphan",
    )

    terminado_detalle = relationship(
        "TerminadoProcesoDetalle",
        back_populates="reporte",
        cascade="all, delete-orphan",
        uselist=False,
    )

    terminado_marcas = relationship(
        "TerminadoMarca",
        back_populates="reporte",
        cascade="all, delete-orphan",
    )