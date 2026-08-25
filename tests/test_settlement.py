"""Tests for 30% settlement / 5–7.5% legal fee rules."""

from fastapi.testclient import TestClient

from app.main import app
from app.settlement import compute_settlement, format_inr

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_one_lakh_remaining_high_fee():
    offer = compute_settlement(100000, fee_percent=7.5, settlement_percent=30)
    assert offer.settlement_amount == 30000.0
    assert offer.fee_amount == 7500.0


def test_one_lakh_remaining_low_fee():
    offer = compute_settlement(100000, fee_percent=5.0)
    assert offer.settlement_amount == 30000.0
    assert offer.fee_amount == 5000.0


def test_rejects_fee_outside_band():
    try:
        compute_settlement(100000, fee_percent=10)
        assert False, "expected error"
    except ValueError as exc:
        assert "5 and 7.5" in str(exc)


def test_rejects_settlement_above_30_percent():
    try:
        compute_settlement(100000, settlement_percent=40)
        assert False, "expected error"
    except ValueError as exc:
        assert "30" in str(exc)


def test_format_inr_indian_grouping():
    assert format_inr(100000) == "₹1,00,000.00"


def test_settlement_api_endpoint():
    response = client.post(
        "/api/v1/settlement/recommend",
        json={"remaining_amount": 100000, "fee_percent": 7.5, "settlement_percent": 30},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["settlement_amount"] == 30000.0
    assert data["fee_amount"] == 7500.0
    assert "summary" in data


def test_invalid_balance_rejected():
    response = client.post(
        "/api/v1/settlement/recommend",
        json={"remaining_amount": -100, "fee_percent": 5},
    )
    assert response.status_code == 422
