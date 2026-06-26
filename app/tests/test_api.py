import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_create_donateur(client: AsyncClient):
    payload = {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@example.com",
        "mot_de_passe": "secret123",
        "type_compte": "enregistre",
    }
    resp = await client.post("/api/v1/donateurs/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "jean.dupont@example.com"
    assert data["nom"] == "Dupont"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_donateur_duplicate(client: AsyncClient):
    payload = {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "duplicate@example.com",
        "mot_de_passe": "secret123",
    }
    resp = await client.post("/api/v1/donateurs/", json=payload)
    assert resp.status_code == 201
    resp2 = await client.post("/api/v1/donateurs/", json=payload)
    assert resp2.status_code == 400


@pytest.mark.asyncio
async def test_list_donateurs(client: AsyncClient):
    resp = await client.get("/api/v1/donateurs/")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_donateur(client: AsyncClient):
    payload = {
        "nom": "Martin",
        "prenom": "Sophie",
        "email": "sophie.martin@example.com",
        "mot_de_passe": "secret123",
    }
    create_resp = await client.post("/api/v1/donateurs/", json=payload)
    donateur_id = create_resp.json()["id"]
    resp = await client.get(f"/api/v1/donateurs/{donateur_id}")
    assert resp.status_code == 200
    assert resp.json()["email"] == "sophie.martin@example.com"


@pytest.mark.asyncio
async def test_get_donateur_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/donateurs/999999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_donateur(client: AsyncClient):
    payload = {
        "nom": "Bernard",
        "prenom": "Luc",
        "email": "luc.bernard@example.com",
        "mot_de_passe": "secret123",
    }
    create_resp = await client.post("/api/v1/donateurs/", json=payload)
    donateur_id = create_resp.json()["id"]
    update = {"telephone": "+33612345678", "pays": "France"}
    resp = await client.patch(f"/api/v1/donateurs/{donateur_id}", json=update)
    assert resp.status_code == 200
    assert resp.json()["telephone"] == "+33612345678"
    assert resp.json()["pays"] == "France"


@pytest.mark.asyncio
async def test_delete_donateur(client: AsyncClient):
    payload = {
        "nom": "Petit",
        "prenom": "Marie",
        "email": "marie.petit@example.com",
        "mot_de_passe": "secret123",
    }
    create_resp = await client.post("/api/v1/donateurs/", json=payload)
    donateur_id = create_resp.json()["id"]
    resp = await client.delete(f"/api/v1/donateurs/{donateur_id}")
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_create_campagne(client: AsyncClient):
    from datetime import datetime, timezone, timedelta
    payload = {
        "titre": "Aide aux sinistrés",
        "description": "Campagne d'urgence",
        "objectif": 50000.0,
        "date_debut": datetime.now(timezone.utc).isoformat(),
        "date_fin": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
    }
    resp = await client.post("/api/v1/campagnes/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["titre"] == "Aide aux sinistrés"
    assert data["objectif"] == 50000.0


@pytest.mark.asyncio
async def test_list_campagnes(client: AsyncClient):
    resp = await client.get("/api/v1/campagnes/")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_create_don(client: AsyncClient):
    from datetime import datetime, timezone, timedelta
    donateur_payload = {
        "nom": "Simon",
        "prenom": "Paul",
        "email": "paul.simon@example.com",
        "mot_de_passe": "secret123",
    }
    d = await client.post("/api/v1/donateurs/", json=donateur_payload)
    donateur_id = d.json()["id"]

    campagne_payload = {
        "titre": "Santé pour tous",
        "objectif": 100000.0,
        "date_debut": datetime.now(timezone.utc).isoformat(),
        "date_fin": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
    }
    c = await client.post("/api/v1/campagnes/", json=campagne_payload)
    campagne_id = c.json()["id"]

    don_payload = {
        "montant": 100.0,
        "donateur_id": donateur_id,
        "campagne_id": campagne_id,
    }
    resp = await client.post("/api/v1/dons/", json=don_payload)
    assert resp.status_code == 201
    assert resp.json()["montant"] == 100.0


@pytest.mark.asyncio
async def test_create_paiement(client: AsyncClient):
    from datetime import datetime, timezone, timedelta
    d = await client.post("/api/v1/donateurs/", json={
        "nom": "Test", "prenom": "User", "email": "test.paiement@example.com",
        "mot_de_passe": "secret",
    })
    donateur_id = d.json()["id"]
    c = await client.post("/api/v1/campagnes/", json={
        "titre": "Test Paiement", "objectif": 1000.0,
        "date_debut": datetime.now(timezone.utc).isoformat(),
        "date_fin": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
    })
    campagne_id = c.json()["id"]
    don = await client.post("/api/v1/dons/", json={
        "montant": 50.0, "donateur_id": donateur_id, "campagne_id": campagne_id,
    })
    don_id = don.json()["id"]

    paiement_payload = {
        "methode": "carte",
        "montant": 50.0,
        "don_id": don_id,
    }
    resp = await client.post("/api/v1/paiements/", json=paiement_payload)
    assert resp.status_code == 201
    assert resp.json()["methode"] == "carte"
    assert "reference" in resp.json()


@pytest.mark.asyncio
async def test_create_recu(client: AsyncClient):
    from datetime import datetime, timezone, timedelta
    d = await client.post("/api/v1/donateurs/", json={
        "nom": "Test2", "prenom": "User2", "email": "test.recu@example.com",
        "mot_de_passe": "secret",
    })
    donateur_id = d.json()["id"]
    c = await client.post("/api/v1/campagnes/", json={
        "titre": "Test Recu", "objectif": 1000.0,
        "date_debut": datetime.now(timezone.utc).isoformat(),
        "date_fin": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
    })
    campagne_id = c.json()["id"]
    don = await client.post("/api/v1/dons/", json={
        "montant": 75.0, "donateur_id": donateur_id, "campagne_id": campagne_id,
    })
    don_id = don.json()["id"]

    resp = await client.post("/api/v1/recus/", json={"don_id": don_id})
    assert resp.status_code == 201
    assert resp.json()["montant"] == 75.0
    assert resp.json()["donateur_nom"] == "User2 Test2"
