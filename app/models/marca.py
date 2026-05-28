from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Marca(Base, TimestampMixin):
    __tablename__ = "marcas"
    __table_args__ = (
        UniqueConstraint("empresa_id", "nombre", name="uq_marca_empresa_nombre"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    activo: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    orden: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    empresa = relationship("Empresa", back_populates="marcas")
