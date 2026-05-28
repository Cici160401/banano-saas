from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ORMBase (BaseModel):
    # permite que Pydantic lea objetos ORM (SQLAlchemy) directamente
    model_config = ConfigDict(from_attributes=True)

class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime

#from_attributes=True (antes orm_mode=True)
#hace que puedas retornar un SQLAlchemy model y Pydantic lo convierta a JSON sin que tú armes dicts a mano.