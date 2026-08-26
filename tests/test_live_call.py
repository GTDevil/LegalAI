"""Tests for live-call readiness and Indian neural voice mapping."""

from fastapi.testclient import TestClient

from app.live_call import azure_voice_id, normalize_e164
from app.main import app

client = TestClient(app)


def test_live_status_not_ready_without_keys(monkeypatch):
    monkeypatch.delenv("VAPI_API_KEY", raising=False)
    monkeypatch.delenv("VAPI_PHONE_NUMBER_ID", raising=False)
    response = client.get("/api/v1/live/status")
    assert response.status_code == 200
    body = response.json()
    assert body["ready"] is False
    assert "VAPI_API_KEY" in body["missing"]
    assert body["voice_woman"] == "hi-IN-SwaraNeural"
    assert body["voice_man"] == "hi-IN-MadhurNeural"
    assert len(body["requirements"]) >= 5


def test_live_call_rejected_without_keys(monkeypatch):
    monkeypatch.delenv("VAPI_API_KEY", raising=False)
    monkeypatch.delenv("VAPI_PHONE_NUMBER_ID", raising=False)
    response = client.post(
        "/api/v1/calls/live",
        json={"name": "Test", "phone": "9876501008", "voice_gender": "woman", "language": "hi"},
    )
    assert response.status_code == 400
    assert "VAPI" in response.json()["detail"]


def test_indian_voice_ids():
    assert azure_voice_id("woman", "hi") == "hi-IN-SwaraNeural"
    assert azure_voice_id("man", "hi") == "hi-IN-MadhurNeural"
    assert azure_voice_id("woman", "en") == "en-IN-NeerjaNeural"


def test_normalize_indian_mobile():
    assert normalize_e164("9876501008") == "+919876501008"
    assert normalize_e164("+919876501008") == "+919876501008"
