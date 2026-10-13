import os, tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.config import get_settings

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("NOVA_DATABASE_PATH", str(tmp_path / "test.sqlite3"))
    get_settings.cache_clear()
    from app.main import app
    with TestClient(app) as c:
        yield c
    get_settings.cache_clear()
