from tests.conftest import auth_headers, create_draft, save_gancho, save_terminado


def test_crear_draft_asigna_empresa_y_permite_header_incompleto(client):
    headers = auth_headers(client, "evaluador@test.com")

    draft = create_draft(
        client,
        headers,
        productor_id=None,
        hacienda_id=None,
        semana_reporte=None,
        fecha_reporte=None,
    )

    assert draft["empresa_id"] == 1
    assert draft["created_by_user_id"] == 2
    assert draft["estado"] == "draft"
    assert draft["productor_id"] is None
    assert draft["hacienda_id"] is None


def test_guardar_gancho_y_detalle(client):
    headers = auth_headers(client)
    draft = create_draft(client, headers)

    save_gancho(client, headers, draft["id"])
    detail = client.get(f"/reportes/{draft['id']}", headers=headers)

    assert detail.status_code == 200
    body = detail.json()
    assert body["gancho_detalle"]["racimos_procesados"] == 90
    assert body["gancho_cintas"][0]["color"]["nombre"] == "NEGRO"
    assert body["gancho_motivos"][0]["motivo"]["nombre"] == "golpeado"


def test_submit_gancho(client):
    headers = auth_headers(client)
    draft = create_draft(client, headers)
    save_gancho(client, headers, draft["id"])

    response = client.post(f"/reportes/{draft['id']}/submit", headers=headers)

    assert response.status_code == 200
    assert response.json()["estado"] == "submitted"
    detail = client.get(f"/reportes/{draft['id']}", headers=headers).json()
    assert detail["historial"][-1]["to_status"] == "submitted"


def test_start_review(client):
    admin_headers = auth_headers(client)
    supervisor_headers = auth_headers(client, "supervisor@test.com")
    draft = create_draft(client, admin_headers)
    save_gancho(client, admin_headers, draft["id"])
    client.post(f"/reportes/{draft['id']}/submit", headers=admin_headers)

    response = client.post(f"/reportes/{draft['id']}/start-review", headers=supervisor_headers)

    assert response.status_code == 200
    assert response.json()["estado"] == "under_review"
    assert response.json()["supervisor_id"] == 3


def test_review_aprobado_y_rechazado(client):
    admin_headers = auth_headers(client)
    supervisor_headers = auth_headers(client, "supervisor@test.com")

    approved = create_draft(client, admin_headers)
    save_gancho(client, admin_headers, approved["id"])
    client.post(f"/reportes/{approved['id']}/submit", headers=admin_headers)
    client.post(f"/reportes/{approved['id']}/start-review", headers=supervisor_headers)
    approved_response = client.post(
        f"/reportes/{approved['id']}/review",
        headers=supervisor_headers,
        json={"accion": "aprobado", "comentario": "ok"},
    )

    rejected = create_draft(client, admin_headers)
    save_gancho(client, admin_headers, rejected["id"])
    client.post(f"/reportes/{rejected['id']}/submit", headers=admin_headers)
    client.post(f"/reportes/{rejected['id']}/start-review", headers=supervisor_headers)
    rejected_response = client.post(
        f"/reportes/{rejected['id']}/review",
        headers=supervisor_headers,
        json={"accion": "rechazado", "comentario": "corregir"},
    )

    assert approved_response.status_code == 200
    assert approved_response.json()["estado"] == "approved"
    assert rejected_response.status_code == 200
    assert rejected_response.json()["estado"] == "needs_changes"


def test_submit_terminado(client):
    headers = auth_headers(client)
    draft = create_draft(client, headers, tipo="terminados_de_proceso")
    save_terminado(client, headers, draft["id"])

    detail = client.get(f"/reportes/{draft['id']}", headers=headers).json()
    assert detail["terminado_detalle"]["total_cajas"] == 15
    assert detail["terminado_detalle"]["evaluador_ci"] == "0900000001"

    response = client.post(f"/reportes/{draft['id']}/submit", headers=headers)
    assert response.status_code == 200
    assert response.json()["estado"] == "submitted"
