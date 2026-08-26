"""The browser calling desk must stay usable with a double-click (no server)."""

from pathlib import Path

from fastapi.testclient import TestClient

from app.call_script import classify_demo_outcome, simulate_call
from app.main import app
from app.workbook import Lead
from run_desktop import calling_desk_html

client = TestClient(app)
HTML = Path("web/index.html").read_text(encoding="utf-8")


def test_html_is_self_contained():
    assert "Start process" in HTML
    assert "Ramesh Nair" in HTML
    assert "9876501008" in HTML
    assert "classifyDemoOutcome" in HTML
    assert "parseLeadsFromText" in HTML
    assert "Import from link" in HTML
    assert "हिन्दी" in HTML
    assert "speechSynthesis" in HTML
    assert "Live setup" in HTML
    assert "hi-IN-SwaraNeural" in HTML or "Swara" in HTML
    assert calling_desk_html().exists()


def test_api_serves_calling_desk():
    response = client.get("/")
    assert response.status_code == 200
    assert "LegalAI calling desk" in response.text
    assert "Start process" in response.text


def test_js_demo_rules_match_python():
    assert classify_demo_outcome("9876501008") == "interested"
    lead = simulate_call(Lead(name="Ramesh Nair", phone="9876501008")).lead
    assert lead.remaining_amount == 100000
    assert lead.settlement_amount == 30000
    assert lead.legal_fee == 5000
    assert "30%" in HTML
