import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from app.core.security import hash_password
from app.db import base_imports  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.cinta_color import CintaColor
from app.models.empresa import Empresa
from app.models.enum import UserRole
from app.models.hacienda import Hacienda
from app.models.hacienda_lote import HaciendaLote
from app.models.marca import Marca
from app.models.motivo_gancho import MotivoGancho
from app.models.productor import Productor
from app.models.user import User


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    seed_data(db)
    db.close()

    def override_get_db() -> Generator[Session, None, None]:
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session: Session) -> TestClient:
    return TestClient(app)


def seed_data(db: Session) -> None:
    empresa = Empresa(id=1, nombre="Empresa Uno")
    otra_empresa = Empresa(id=2, nombre="Empresa Dos")
    db.add_all([empresa, otra_empresa])

    users = [
        User(
            id=1,
            empresa_id=1,
            nombre="Admin Uno",
            identificacion="0900000001",
            email="admin@test.com",
            password_hash=hash_password("123456"),
            role=UserRole.admin,
            is_active=True,
        ),
        User(
            id=2,
            empresa_id=1,
            nombre="Evaluador Uno",
            identificacion="0900000002",
            email="evaluador@test.com",
            password_hash=hash_password("123456"),
            role=UserRole.evaluador,
            is_active=True,
        ),
        User(
            id=3,
            empresa_id=1,
            nombre="Supervisor Uno",
            identificacion="0900000003",
            email="supervisor@test.com",
            password_hash=hash_password("123456"),
            role=UserRole.supervisor,
            is_active=True,
        ),
        User(
            id=4,
            empresa_id=2,
            nombre="Admin Dos",
            identificacion="0900000004",
            email="admin2@test.com",
            password_hash=hash_password("123456"),
            role=UserRole.admin,
            is_active=True,
        ),
    ]
    db.add_all(users)

    productor = Productor(
        id=1,
        empresa_id=1,
        codigo_productor=101,
        nombre="Productor Prueba",
        identificacion="0999999999",
        telefono="0990000000",
    )
    hacienda = Hacienda(
        id=1,
        empresa_id=1,
        productor_id=1,
        codigo_hacienda=201,
        nombre="Hacienda Prueba",
        zona="Zona Norte",
    )
    db.add_all([productor, hacienda])
    db.add_all(
        [
            HaciendaLote(id=1, hacienda_id=1, numero_lote=1),
            HaciendaLote(id=2, hacienda_id=1, numero_lote=2),
        ]
    )

    db.add_all(
        [
            CintaColor(id=1, empresa_id=1, nombre="NEGRO", hex="#000000", activo=1, orden=1),
            CintaColor(id=2, empresa_id=1, nombre="VERDE", hex="#008000", activo=1, orden=2),
            MotivoGancho(id=1, empresa_id=1, nombre="golpeado", activo=1, orden=1),
            MotivoGancho(id=2, empresa_id=1, nombre="manchado", activo=1, orden=2),
            Marca(id=1, empresa_id=1, nombre="Banana Prime", activo=1, orden=1),
            Marca(id=2, empresa_id=1, nombre="Tropical Gold", activo=1, orden=2),
            Marca(id=3, empresa_id=2, nombre="Marca Otra Empresa", activo=1, orden=1),
        ]
    )

    db.commit()


def auth_headers(client: TestClient, email: str = "admin@test.com") -> dict[str, str]:
    response = client.post(
        "/auth/login",
        data={"username": email, "password": "123456"},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_draft(
    client: TestClient,
    headers: dict[str, str],
    *,
    tipo: str = "reporte_de_gancho",
    productor_id: int | None = 1,
    hacienda_id: int | None = 1,
    semana_reporte: int | None = 35,
    fecha_reporte: str | None = "2025-08-28",
) -> dict:
    response = client.post(
        "/reportes/drafts",
        headers=headers,
        json={
            "empresa_id": 999,
            "productor_id": productor_id,
            "hacienda_id": hacienda_id,
            "tipo": tipo,
            "semana_reporte": semana_reporte,
            "fecha_reporte": fecha_reporte,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def save_gancho(client: TestClient, headers: dict[str, str], reporte_id: int) -> dict:
    response = client.put(
        f"/reportes/{reporte_id}/gancho",
        headers=headers,
        json={
            "detalle": {
                "cupo_total": 100,
                "racimos_cosechados": 95,
                "racimos_procesados": 90,
                "racimos_rechazados": 5,
                "observaciones": "ok",
            },
            "cintas": [{"semanas": 12, "descripcion": "cinta 1", "color_id": 1, "cantidad": 10}],
            "motivos": [{"motivo_id": 1, "cantidad": 5}],
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def save_terminado(client: TestClient, headers: dict[str, str], reporte_id: int) -> dict:
    response = client.put(
        f"/reportes/{reporte_id}/terminado",
        headers=headers,
        json={
            "detalle": {
                "exportadora": "ASOGUABO",
                "camion": "1",
                "puerto_acopio": "ASO GUABO",
                "codigo": "(5451)(9552)",
                "cupo_completo": 15,
                "sello_plastico": "AG25298",
                "placa": "OAA2267",
                "chofer_nombre": "Pablo Nunez",
                "chofer_ci": "0701284358",
                "chofer_telefono": "0990740405",
                "calificador_nombre": "Segundo Merchan",
                "hora_termino": "16:30:00",
            },
            "lotes": [
                {
                    "numero_lote": 1,
                    "marcas": [
                        {"marca_id": 1, "cajas": 10},
                        {"marca": "ALL GOOD CINTA", "cajas": 5},
                    ],
                }
            ],
        },
    )
    assert response.status_code == 200, response.text
    return response.json()
