# backend/app/tests/test_endpoints.py
# Minimal tests — you can run via pytest after installing dev deps

from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "HR Resource Query Chatbot" in r.json().get("message","") or "API" in r.json().get("message","")
