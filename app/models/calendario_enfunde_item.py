from sqlalchemy import Integer, ForeignKey, DateTime, func, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.mixins import TimestampMixin

from app.db.base import Base


class CalendarioEnfundeItem(Base, TimestampMixin):
    __tablename__ = "calendario_enfunde_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    #LLAMAMOS AL ID DEL CALENDARIO, DE LA TABLA CALENDARIOS_ENFUNDE
    calendario_id: Mapped[int] = mapped_column(ForeignKey("calendarios_enfunde.id"), nullable=False, index=True)
    #ES EL NUMERO DE LA SEMANA
    semana: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..53 o 9..14 según tu caso
    #LLAMAMOS AL ID DE LA CINTA, DE LA TABLA CINTA_COLORES
    color_id: Mapped[int] = mapped_column(ForeignKey("cinta_colores.id"), nullable=False, index=True)
    #ES EL CODIGO DEL COLOR, ES DECIR  ROJO = 1, VERDE= 4, ETC...
    codigo: Mapped[int] = mapped_column(Integer, nullable=False)  # número de la tablita (1,2,3,...)
    #Creado en "fecha"
    #created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    
    #Establecemos relacion con la tabla calendarioEnfunde
    calendario = relationship("CalendarioEnfunde", back_populates="items")
    #Establecemos relacion con la tabla CintaColor
    color = relationship("CintaColor", back_populates="calendario_items")

    __table_args__ = (
        # No repetir el mismo color en la misma semana dentro del mismo calendario
        UniqueConstraint("calendario_id", "semana", "color_id", name="uq_cal_semana_color"),
        # No repetir el mismo codigo en la misma semana dentro del mismo calendario
        UniqueConstraint("calendario_id", "semana", "codigo", name="uq_cal_semana_codigo"),
        Index("ix_cal_semana", "calendario_id", "semana"),
    )
