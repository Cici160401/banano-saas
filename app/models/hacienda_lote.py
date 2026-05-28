from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin
from app.db.base import Base

class HaciendaLote(Base, TimestampMixin):
    __tablename__ = "hacienda_lotes"
    __table_args__ = (
        UniqueConstraint("hacienda_id", "numero_lote", name="uq_hacienda_numero_lote"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hacienda_id: Mapped[int] = mapped_column(ForeignKey("haciendas.id"), nullable=False, index=True)
    numero_lote: Mapped[int] = mapped_column(Integer, nullable=False)

    hacienda = relationship("Hacienda", back_populates="lotes")