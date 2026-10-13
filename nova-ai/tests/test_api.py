def test_health_and_settings(client):
    assert client.get("/api/health").status_code == 200
    assert client.get("/api/settings").json()["name"]

def test_conversation_crud(client):
    c = client.post("/api/conversations").json()
    cid = c["id"]
    assert client.get(f"/api/conversations/{cid}/messages").json() == []
    r = client.patch(f"/api/conversations/{cid}", json={"title":"Essai"})
    assert r.status_code == 200 and r.json()["title"] == "Essai"
    assert client.delete(f"/api/conversations/{cid}").json()["deleted"] is True
    assert client.get(f"/api/conversations/{cid}/messages").status_code == 404

def test_memory_crud(client):
    item = client.post("/api/memory", json={"content":"Répondre en français"}).json()
    assert item["id"]
    assert len(client.get("/api/memory").json()) == 1
    assert client.delete(f"/api/memory/{item['id']}").status_code == 200
    assert client.get("/api/memory").json() == []

def test_document_ingestion_and_retrieval(client):
    result = client.post("/api/documents", files={"file":("guide.txt",b"Le projet NOVA utilise FastAPI et SQLite.", "text/plain")})
    assert result.status_code == 200
    assert client.get("/api/documents").json()[0]["filename"] == "guide.txt"
    assert client.post("/api/documents", files={"file":("guide.txt",b"Le projet NOVA utilise FastAPI et SQLite.", "text/plain")}).json()["duplicate"]
    # retrieval is integrated into chat context; endpoint itself remains internal.
    assert client.delete(f"/api/documents/{result.json()['id']}").json()["deleted"]

def test_reject_unsupported_document(client):
    r = client.post("/api/documents", files={"file":("bad.exe",b"nope","application/octet-stream")})
    assert r.status_code == 400

def test_frontend_served(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "NOVA AI" in r.text
