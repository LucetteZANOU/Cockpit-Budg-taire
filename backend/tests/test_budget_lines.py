from fastapi.testclient import TestClient


def _create_line(client: TestClient, **overrides) -> dict:
    payload = {
        "categorie": "Marketing",
        "montant_prevu": "1000.00",
        "montant_realise": "800.00",
        "periode": "2026-01",
        **overrides,
    }
    response = client.post("/api/budget-lines", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_budget_line(client: TestClient) -> None:
    data = _create_line(client)
    assert data["categorie"] == "Marketing"
    assert data["ecart_valeur"] == "-200.00"
    assert data["ecart_pourcentage"] == "-20.00"


def test_list_budget_lines_with_filters(client: TestClient) -> None:
    _create_line(client, categorie="Marketing", periode="2026-01")
    _create_line(client, categorie="Ventes", periode="2026-02")

    response = client.get("/api/budget-lines", params={"categorie": "Marketing"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["categorie"] == "Marketing"


def test_get_budget_line(client: TestClient) -> None:
    created = _create_line(client)
    response = client.get(f"/api/budget-lines/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_budget_line_not_found(client: TestClient) -> None:
    response = client.get("/api/budget-lines/999")
    assert response.status_code == 404


def test_update_budget_line(client: TestClient) -> None:
    created = _create_line(client)
    response = client.patch(
        f"/api/budget-lines/{created['id']}", json={"montant_realise": "1200.00"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["montant_realise"] == "1200.00"
    assert data["ecart_valeur"] == "200.00"


def test_delete_budget_line(client: TestClient) -> None:
    created = _create_line(client)
    response = client.delete(f"/api/budget-lines/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/api/budget-lines/{created['id']}")
    assert response.status_code == 404


def test_summary(client: TestClient) -> None:
    _create_line(client, categorie="Marketing", montant_prevu="1000.00", montant_realise="800.00")
    _create_line(client, categorie="Ventes", montant_prevu="500.00", montant_realise="600.00")

    response = client.get("/api/budget-lines/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_prevu"] == "1500.00"
    assert data["total_realise"] == "1400.00"
    assert len(data["par_categorie"]) == 2
