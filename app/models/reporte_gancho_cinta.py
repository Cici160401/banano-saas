from decimal import Decimal

from sqlalchemy import Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin

from app.db.base import Base


class ReporteGanchoCinta(Base, TimestampMixin):
    __tablename__ = "reporte_gancho_cintas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    reporte_id: Mapped[int] = mapped_column(ForeignKey("reportes.id"), nullable=False, index=True)

    # 12, 11, 10...
    semanas: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # opcional: "BARRIDA", "CALIBRADA", o notas tipo "Amarilla 350"
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # FK al catálogo por empresa
    color_id: Mapped[int | None] = mapped_column(ForeignKey("cinta_colores.id"), nullable=True, index=True)

    cantidad: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # DECIMAL debe mapearse a Decimal, no a str
    porcentaje: Mapped[Decimal | None] = mapped_column(DECIMAL(6, 2), nullable=True)

    reporte = relationship("Reporte", back_populates="gancho_cintas")
    color = relationship("CintaColor", back_populates="reporte_cintas")
