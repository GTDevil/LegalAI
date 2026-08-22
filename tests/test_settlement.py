"""Tests for settlement recommendation logic."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.settlement import LoanCase, recommend_settlement

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_recommend_settlement_recent_default():
    case = LoanCase(
        principal=50000,
        outstanding_balance=45000,
        days_past_due=15,
        borrower_income=60000,
    )
    offer = recommend_settlement(case)
    assert offer.discount_percent == 5.0
    assert offer.recommended_amount == 42750.0
    assert offer.payment_terms_months == 3


def test_recommend_settlement_severely_delinquent():
    case = LoanCase(
        principal=100000,
        outstanding_balance=80000,
        days_past_due=200,
        borrower_income=5000,
        prior_settlements=0,
    )
    offer = recommend_settlement(case)
    assert offer.discount_percent >= 40.0
    assert offer.payment_terms_months == 12


def test_settlement_api_endpoint():
    response = client.post(
        "/api/v1/settlement/recommend",
        json={
            "principal": 50000,
            "outstanding_balance": 40000,
            "days_past_due": 90,
            "borrower_income": 55000,
            "prior_settlements": 0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["recommended_amount"] < 40000
    assert data["discount_percent"] > 0
    assert "rationale" in data


def test_invalid_balance_rejected():
    response = client.post(
        "/api/v1/settlement/recommend",
        json={
            "principal": 50000,
            "outstanding_balance": -100,
            "days_past_due": 30,
            "borrower_income": 50000,
        },
    )
    assert response.status_code == 422
