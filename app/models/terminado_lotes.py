from sqlalchemy import Integer, String, Text, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin
from datetime import time
from app.db.base import Base

class TerminadoLote(Base, TimestampMixin):
    __tablename__ = "terminado_lotes"

    id = mapped_column(Integer, primary_key=True)
    numero_lote = mapped_column(Integer, nullable=False)
    terminado_detalle_id = mapped_column(ForeignKey("terminado_proceso_detalles.id"),nullable=False,index=True)

    terminado_detalle = relationship(
        "TerminadoProcesoDetalle",
        back_populates="lotes"
    )

    marcas = relationship(
        "TerminadoLoteMarca",
        back_populates="lote",
        cascade="all, delete-orphan",
    )