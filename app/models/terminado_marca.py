from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TerminadoMarca(Base):
    __tablename__ = "terminado_marcas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reporte_id: Mapped[int] = mapped_column(ForeignKey("reportes.id"), nullable=False)

    marca: Mapped[str] = mapped_column(String(150), nullable=False)
    cajas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    reporte = relationship("Reporte", back_populates="terminado_marcas")
