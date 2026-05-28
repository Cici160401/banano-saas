from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin

from app.db.base import Base

class Empresa(Base, TimestampMixin):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)

    users = relationship(
        "User",
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    haciendas = relationship("Hacienda", back_populates="empresa")
    #RELACIÓN DE CADA CALENDARIO ED ENFUNDE CON CADA EMPRESA
    cinta_colores = relationship("CintaColor", back_populates="empresa", cascade="all, delete-orphan")
    marcas = relationship("Marca", back_populates="empresa", cascade="all, delete-orphan")
    #RELACIÓN DE CADA CALENDARIO DE ENFUNDE CON SU EMPRESA
    calendarios_enfunde = relationship("CalendarioEnfunde", back_populates="empresa", cascade="all, delete-orphan")
