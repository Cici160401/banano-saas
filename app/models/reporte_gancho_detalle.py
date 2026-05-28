from sqlalchemy import Integer, Text, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin
from decimal import Decimal

from app.db.base import Base

class ReporteGanchoDetalle (Base,TimestampMixin):
    __tablename__= "reporte_gancho_detalles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    #1 a 1: un detalle por reporte solo si es tipo=gancho
    reporte_id: Mapped[int] = mapped_column(ForeignKey("reportes.id"), nullable=False, unique=True)   
    
    hectareas: Mapped[Decimal | None] = mapped_column(DECIMAL(10,2), nullable=True)
    cupo_total: Mapped[int | None] = mapped_column(Integer, nullable=True)

    calendario_enfunde: Mapped[str | None] = mapped_column(Text, nullable=True)
    #ES EL RACIMO, ENCAPSULADO EN LA BELLOTA, LO QUE QUIERE DECIR EL COLOR ES LA SEMANA CUANDO PARIÓ LA MATA
    bellota_cucula: Mapped[str | None] = mapped_column(Text, nullable=True)

    racimos_cosechados: Mapped[int | None] = mapped_column(Integer, nullable=True)
    racimos_procesados: Mapped[int | None] = mapped_column(Integer, nullable=True)
    racimos_rechazados: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # lo puedes calcular en backend, pero igual lo guardamos por auditoría
    ratio: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 4), nullable=True)

    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    #ESTABLECEMOS LA RELACIÓN CON EL REPORTE, LA TABLA MADRE
    reporte = relationship("Reporte", back_populates="gancho_detalle")