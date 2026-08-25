"""Tests for workbook import/export and demo calling agent."""

from pathlib import Path

from fastapi.testclient import TestClient

from app.call_agent import CampaignController
from app.call_script import classify_demo_outcome, simulate_call
from app.main import app
from app.settings import AppSettings
from app.workbook import Lead, load_workbook_file, save_workbook_file

client = TestClient(app)


def test_demo_outcomes_by_last_digit():
    assert classify_demo_outcome("9876543210") == "no_answer"
    assert classify_demo_outcome("9876543211") == "not_interested"
    assert classify_demo_outcome("9876543213") == "no_loan"
    assert classify_demo_outcome("9876543214") == "interested"


def test_simulate_interested_fills_settlement_fields():
    result = simulate_call(Lead(name="Priya Sharma", phone="9876543214"), firm_name="Demo Firm")
    lead = result.lead
    assert result.outcome == "interested"
    assert lead.interested == "Yes"
    assert lead.remaining_amount is not None
    assert lead.settlement_amount == round(lead.remaining_amount * 0.30, 2)
    assert lead.legal_fee in {
        round(lead.remaining_amount * 0.05, 2),
        round(lead.remaining_amount * 0.075, 2),
    }
    assert lead.cibil_or_experience.startswith("CIBIL")
    assert lead.call_status == "Completed"


def test_simulate_not_interested():
    result = simulate_call(Lead(name="Rahul", phone="9876543211"))
    assert result.lead.interested == "No"
    assert result.lead.call_status == "Not interested"
    assert result.lead.settlement_amount is None


def test_campaign_updates_sample_sheet(tmp_path: Path):
    source = Path("data/sample_leads.csv")
    leads = load_workbook_file(source)
    settings = AppSettings(firm_name="Test Firm", call_mode="demo", seconds_between_calls=0)
    report = CampaignController().run(leads, settings)
    assert report.attempted == 8
    output = tmp_path / "updated.xlsx"
    save_workbook_file(output, leads)
    reloaded = load_workbook_file(output)
    priya = next(row for row in reloaded if row.name == "Priya Sharma")
    assert priya.interested == "Yes"
    assert priya.settlement_amount is not None
    rahul = next(row for row in reloaded if row.name == "Rahul Verma")
    assert rahul.call_status == "No answer"


def test_simulate_api():
    response = client.post(
        "/api/v1/calls/simulate",
        json={"name": "Priya Sharma", "phone": "9876543214", "firm_name": "API Firm"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == "interested"
    assert body["lead"]["interested"] == "Yes"


def test_campaign_api_skips_blank_phone():
    response = client.post(
        "/api/v1/campaign/demo",
        json={
            "firm_name": "API Firm",
            "leads": [
                {"name": "Priya", "phone": "9876543214"},
                {"name": "Nobody", "phone": ""},
            ],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["attempted"] == 1
    assert body["leads"][0]["interested"] == "Yes"
