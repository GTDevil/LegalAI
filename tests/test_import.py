"""Tests for bulk import URL safety and Google Sheet rewriting."""

from fastapi.testclient import TestClient

from app.main import app
from app.url_fetch import normalize_sheet_url

client = TestClient(app)


def test_normalize_google_sheet_edit_link():
    url = "https://docs.google.com/spreadsheets/d/abc123XYZ/edit#gid=7"
    assert normalize_sheet_url(url) == (
        "https://docs.google.com/spreadsheets/d/abc123XYZ/export?format=csv&gid=7"
    )


def test_import_rejects_localhost():
    response = client.post("/api/v1/import/from-url", json={"url": "https://127.0.0.1/leads.csv"})
    assert response.status_code == 400


def test_import_rejects_http():
    response = client.post("/api/v1/import/from-url", json={"url": "http://example.com/leads.csv"})
    assert response.status_code == 400
