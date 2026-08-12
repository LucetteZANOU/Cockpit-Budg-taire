from fastapi.testclient import TestClient


def _create_centre_cout(client: TestClient, nom: str = "Marketing") -> dict:
    response = client.post("/api/centres-cout", json={"nom": nom})
    assert response.status_code == 201
    return response.json()


def _create_line(client: TestClient, centre_cout_id: int, **overrides) -> dict:
    payload = {
        "centre_cout_id": centre_cout_id,
        "exercice": 2026,
        "periode": "2026-01",
        "montant_prevu": "1000.00",
        "montant_realise": "800.00",
        **overrides,
    }
    response = client.post("/api/budget-lines", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_centre_cout(client: TestClient) -> None:
    data = _create_centre_cout(client)
    assert data["nom"] == "Marketing"


def test_create_centre_cout_duplicate(client: TestClient) -> None:
    _create_centre_cout(client)
    response = client.post("/api/centres-cout", json={"nom": "Marketing"})
    assert response.status_code == 409


def test_create_budget_line(client: TestClient) -> None:
    centre = _create_centre_cout(client)
    data = _create_line(client, centre["id"])
    assert data["centre_cout"]["nom"] == "Marketing"
    assert data["exercice"] == 2026
    assert data["ecart_valeur"] == "-200.00"
    assert data["ecart_pourcentage"] == "-20.00"
    assert data["montant_reestime"] is None
    assert data["ecart_reestime_valeur"] is None


def test_create_budget_line_exercice_mismatch(client: TestClient) -> None:
    centre = _create_centre_cout(client)
    response = client.post(
        "/api/budget-lines",
        json={
            "centre_cout_id": centre["id"],
            "exercice": 2025,
            "periode": "2026-01",
            "montant_prevu": "1000.00",
            "montant_realise": "800.00",
        },
    )
    assert response.status_code == 422


def test_create_budget_line_with_reestime(client: TestClient) -> None:
    centre = _create_centre_cout(client)
    data = _create_line(client, centre["id"], montant_reestime="1100.00")
    assert data["ecart_reestime_valeur"] == "100.00"
    assert data["ecart_reestime_pourcentage"] == "10.00"


def test_list_budget_lines_with_filters(client: TestClient) -> None:
    marketing = _create_centre_cout(client, "Marketing")
    ventes = _create_centre_cout(client, "Ventes")
    _create_line(client, marketing["id"], periode="2026-01")
    _create_line(client, ventes["id"], periode="2026-02", exercice=2026)

    response = client.get("/api/budget-lines", params={"centre_cout_id": marketing["id"]})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["centre_cout"]["nom"] == "Marketing"


def test_get_budget_line(client: TestClient) -> None:
    centre = _create_centre_cout(client)
    created = _create_line(client, centre["id"])
    response = client.get(f"/api/budget-lines/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_budget_line_not_found(client: TestClient) -> None:
    response = client.get("/api/budget-lines/999")
    assert response.status_code == 404


def test_update_budget_line(client: TestClient) -> None:
    centre = _create_centre_cout(client)
    created = _create_line(client, centre["id"])
    response = client.patch(
        f"/api/budget-lines/{created['id']}", json={"montant_realise": "1200.00"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["montant_realise"] == "1200.00"
    assert data["ecart_valeur"] == "200.00"


def test_delete_budget_line(client: TestClient) -> None:
    centre = _create_centre_cout(client)
    created = _create_line(client, centre["id"])
    response = client.delete(f"/api/budget-lines/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/api/budget-lines/{created['id']}")
    assert response.status_code == 404


def test_summary(client: TestClient) -> None:
    marketing = _create_centre_cout(client, "Marketing")
    ventes = _create_centre_cout(client, "Ventes")
    _create_line(client, marketing["id"], montant_prevu="1000.00", montant_realise="800.00")
    _create_line(client, ventes["id"], montant_prevu="500.00", montant_realise="600.00")

    response = client.get("/api/budget-lines/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_prevu"] == "1500.00"
    assert data["total_realise"] == "1400.00"
    assert data["total_reestime"] is None
    assert len(data["par_centre_cout"]) == 2


def test_summary_with_reestime(client: TestClient) -> None:
    marketing = _create_centre_cout(client, "Marketing")
    _create_line(client, marketing["id"], montant_prevu="1000.00", montant_reestime="1100.00")

    response = client.get("/api/budget-lines/summary")
    data = response.json()
    assert data["total_reestime"] == "1100.00"
    assert data["ecart_reestime_valeur"] == "100.00"
