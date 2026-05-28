from tests.conftest import auth_headers


def test_catalogos_filtrados_por_empresa(client):
    admin_headers = auth_headers(client, "admin@test.com")
    other_headers = auth_headers(client, "admin2@test.com")

    colores = client.get("/catalogos/colores", headers=admin_headers)
    motivos = client.get("/catalogos/motivos", headers=admin_headers)
    marcas = client.get("/catalogos/marcas", headers=admin_headers)
    marcas_otra_empresa = client.get("/catalogos/marcas", headers=other_headers)

    assert colores.status_code == 200
    assert motivos.status_code == 200
    assert marcas.status_code == 200
    assert [item["nombre"] for item in colores.json()] == ["NEGRO", "VERDE"]
    assert [item["nombre"] for item in motivos.json()] == ["golpeado", "manchado"]
    assert [item["nombre"] for item in marcas.json()] == ["Banana Prime", "Tropical Gold"]
    assert marcas_otra_empresa.json() == ["Marca Otra Empresa"] or marcas_otra_empresa.json() == [
        {"id": 3, "nombre": "Marca Otra Empresa"}
    ]
