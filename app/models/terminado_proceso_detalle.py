from sqlalchemy import Integer, String, Text, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin
from datetime import time
from app.db.base import Base


class TerminadoProcesoDetalle(Base,TimestampMixin):
    __tablename__ = "terminado_proceso_detalles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reporte_id: Mapped[int] = mapped_column(ForeignKey("reportes.id"), nullable=False, unique=True)


    exportadora: Mapped[str | None] = mapped_column(String(150), nullable=True)
    camion: Mapped[str | None] = mapped_column(String(50), nullable=True)

    vapor: Mapped[str | None] = mapped_column(String(120), nullable=True)

    puerto_acopio: Mapped[str | None] = mapped_column(String(150), nullable=True)
    codigo: Mapped[str | None] = mapped_column(String(120), nullable=True)  # "(5451)(9552)"

    total_cajas: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cupo_completo: Mapped[int | None] = mapped_column(Integer, nullable=True)

    sello_plastico: Mapped[str | None] = mapped_column(String(80), nullable=True)
    placa: Mapped[str | None] = mapped_column(String(30), nullable=True)

    chofer_nombre: Mapped[str | None] = mapped_column(String(120), nullable=True)
    chofer_ci: Mapped[str | None] = mapped_column(String(30), nullable=True)
    chofer_telefono: Mapped[str | None] = mapped_column(String(30), nullable=True)

    evaluador_nombre_texto: Mapped[str | None] = mapped_column(String(120), nullable=True)  # si quieres guardar “tal cual”
    evaluador_ci: Mapped[str | None] = mapped_column(String(30), nullable=True)
    calificador_nombre: Mapped[str | None] = mapped_column(String(120), nullable=True)

    hora_termino: Mapped[time | None] = mapped_column(Time, nullable=True)

    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    reporte = relationship("Reporte", back_populates="terminado_detalle")

    lotes = relationship("TerminadoLote",back_populates="terminado_detalle",cascade="all, delete-orphan")
