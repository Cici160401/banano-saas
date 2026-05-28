# app/api/v1/api.py
from fastapi import APIRouter

from app.api.v1.endpoints import reportes
from app.api.v1.endpoints import gancho  # crea este archivo si aún no existe

api_router = APIRouter()

api_router.include_router(reportes.router)
api_router.include_router(gancho.router)