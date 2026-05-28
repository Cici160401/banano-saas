from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin

from app.db.base import Base

class Hacienda(Base, TimestampMixin):
    __tablename__ = "haciendas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    productor_id: Mapped[int] = mapped_column(ForeignKey("productores.id"), nullable=False)

    codigo_hacienda: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    zona: Mapped[str] = mapped_column(String(100), nullable=False)

    direccion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hectareas: Mapped[int | None] = mapped_column(Integer, nullable=True)

    productor = relationship("Productor", back_populates="haciendas")
    empresa = relationship("Empresa", back_populates="haciendas")

    reportes = relationship("Reporte", back_populates="hacienda")
    lotes = relationship("HaciendaLote", back_populates="hacienda", cascade="all, delete-orphan")
