from tests.conftest import auth_headers, create_draft, save_gancho


def test_filtros_busqueda_y_paginacion(client):
    admin_headers = auth_headers(client)
    supervisor_headers = auth_headers(client, "supervisor@test.com")
    evaluador_headers = auth_headers(client, "evaluador@test.com")

    first = create_draft(
        client,
        admin_headers,
        semana_reporte=35,
        fecha_reporte="2025-08-28",
    )
    save_gancho(client, admin_headers, first["id"])
    client.post(f"/reportes/{first['id']}/submit", headers=admin_headers)

    second = create_draft(
        client,
        admin_headers,
        semana_reporte=36,
        fecha_reporte="2025-08-29",
    )

    own = create_draft(
        client,
        evaluador_headers,
        semana_reporte=37,
        fecha_reporte="2025-08-30",
    )

    submitted = client.get("/reportes?estado=submitted", headers=supervisor_headers)
    week = client.get("/reportes?semana_reporte=36", headers=supervisor_headers)
    search = client.get("/reportes?search=Prueba", headers=supervisor_headers)
    paged = client.get("/reportes?limit=1&offset=1&order_by=id&order_dir=asc", headers=supervisor_headers)
    evaluador_list = client.get("/reportes", headers=evaluador_headers)

    assert submitted.status_code == 200
    assert submitted.json()["total"] == 1
    assert submitted.json()["items"][0]["id"] == first["id"]
    assert week.json()["total"] == 1
    assert week.json()["items"][0]["id"] == second["id"]
    assert search.json()["total"] >= 3
    assert paged.json()["limit"] == 1
    assert len(paged.json()["items"]) == 1
    assert evaluador_list.json()["total"] == 1
    assert evaluador_list.json()["items"][0]["id"] == own["id"]
