from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin

from app.db.base import Base


class CalendarioEnfunde(Base, TimestampMixin):
    __tablename__ = "calendarios_enfunde"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    #LLAMAMOS AL ID DE LA EMPRESA, SEGUN ESO ES EL CALENDARIO
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False, index=True)

    anio: Mapped[int] = mapped_column(Integer, nullable=False)  # 2026, 2027...
    nombre: Mapped[str] = mapped_column(String(120), nullable=False, default="Calendario")
    activo: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    #created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    #updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    #ESTABLECEMOS LA RELACIÓN ENTRE EL CALENDARIO Y LA EMPRESA
    empresa = relationship("Empresa", back_populates="calendarios_enfunde")
    #ESTABLECEMOS LA RELACIÓN ENTRE EL CALENDARIO Y EL CALENDARIO DE ENFUNDE ITEM
    items = relationship("CalendarioEnfundeItem", back_populates="calendario", cascade="all, delete-orphan")
