from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine
from fastapi import APIRouter

from app.api.v1.endpoints import reportes
from app.api.v1.endpoints import gancho 
from app.api.v1.endpoints import terminado
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import catalogos
from app.api.v1.endpoints import haciendas
from app.api.v1.endpoints import productores

from app.db import base_imports  # noqa: F401

app = FastAPI(title="Banano SaaS API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        value = conn.execute(text("SELECT 1")).scalar_one()
    return {"db": "ok", "result": value}


api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(reportes.router)
api_router.include_router(gancho.router)
api_router.include_router(terminado.router)
api_router.include_router(catalogos.router)
api_router.include_router(productores.router)
api_router.include_router(haciendas.router)


app.include_router(api_router)
