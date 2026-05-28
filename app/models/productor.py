from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin
from app.db.base import Base

class Productor(Base, TimestampMixin):
    __tablename__ = "productores"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    codigo_productor: Mapped[int] = mapped_column(Integer, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    identificacion: Mapped[str | None] = mapped_column(String(50), nullable=True)  # cédula/RUC opcional
    telefono: Mapped[str | None] = mapped_column(String(50), nullable=True)

    #created_at: Mapped["DateTime"] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    #updated_at: Mapped["DateTime"] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # relaciones
    haciendas = relationship("Hacienda", back_populates="productor", cascade="all, delete-orphan")
    empresa = relationship("Empresa")
    reportes = relationship("Reporte", back_populates="productor")