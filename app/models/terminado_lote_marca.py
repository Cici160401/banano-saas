from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.mixins import TimestampMixin

class TerminadoLoteMarca(Base, TimestampMixin):
    __tablename__ = "terminado_lote_marcas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    lote_id: Mapped[int] = mapped_column(ForeignKey("terminado_lotes.id"), nullable=False, index=True)

    marca: Mapped[str] = mapped_column(String(150), nullable=False)
    cajas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    lote = relationship("TerminadoLote", back_populates="marcas")
