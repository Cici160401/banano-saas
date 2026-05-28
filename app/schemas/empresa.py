
#Los schemas (Pydantic) sirven para 3 cosas:
#Validar lo que entra (request body).
#Ej: que semana_reporte sea int, que fecha_reporte sea date, que no falten campos cuando “envías”.
#Controlar lo que sale (response).
#Ej: nunca devolver password_hash, o devolver empresa resumida.
#Separar tipos de operaciones:
#Create → datos mínimos para crear
#Update → todos opcionales (para editar)
#Read/Out → lo que se devuelve al cliente (incluye id, created_at)
#📌 Regla mental:
#Model = BD | Schema = contrato de tu API.


#A DIFERENCIA DE LOS PROCESOS ANTERIORES, CUANDO VAMOS A MOSTRAR DATOS DESDE LA BD
#NECESITAMOS ACLARAR QUE LO QUE LLEGARÁ NO ES UN JSON SINO UN OBJETO DE SQLALCHEMY
#POR LO TANTO NECESITAMOS CONFIGURAR EL MODELO (CONFIGDICT) PERO ESPECIFICANDO QUE
#NO ES UN JSON, POR LO TANTO PONEMOS FROM_ATTRIBUTES:TRUE
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

class EmpresaBase(BaseModel):
    nombre: str = Field(..., max_length=200)

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaOut(ORMBase):
    id: int
    nombre: str

#SCHEMA PARA MOSTRAR Y DEVOLVER EN EL FRONTEND
class EmpresaBasicOut(ORMBase):
    id: int
    nombre: str