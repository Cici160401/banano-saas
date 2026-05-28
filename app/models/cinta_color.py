from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin
from app.db.base import Base


class CintaColor(Base, TimestampMixin):
    __tablename__ = "cinta_colores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    #LLAMAMOS AL ID DE LA EMPRESA PARA OBTENER LA CINTA
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False, index=True)

    nombre: Mapped[str] = mapped_column(String(50), nullable=False)  # "NEGRO", "VERDE", ...
    hex: Mapped[str | None] = mapped_column(String(15), nullable=True)  # "#000000" opcional
    activo: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    orden: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    #created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    #updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    #ESTABLECEMOS LA RELACIÓN ENTRE EMPRESA Y LAS CINTAS
    empresa = relationship("Empresa", back_populates="cinta_colores")

    # Relación con items del calendario
    calendario_items = relationship("CalendarioEnfundeItem", back_populates="color", cascade="all, delete-orphan")

    # Relación con cintas del reporte (si ya tienes ReporteCinta)
    reporte_cintas = relationship("ReporteGanchoCinta", back_populates="color")