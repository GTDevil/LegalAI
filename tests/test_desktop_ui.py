"""Tests for desktop UI helpers."""

import tkinter as tk

import pytest

pytest.importorskip("tkinter")

from app.desktop_ui import SettlementDesktopApp


@pytest.fixture
def desktop_app():
    root = tk.Tk()
    root.withdraw()
    app = SettlementDesktopApp(root)
    yield app
    root.destroy()


def test_calculate_updates_results(desktop_app):
    desktop_app.fields["principal"].delete(0, tk.END)
    desktop_app.fields["principal"].insert(0, "50000")
    desktop_app.fields["outstanding_balance"].delete(0, tk.END)
    desktop_app.fields["outstanding_balance"].insert(0, "40000")
    desktop_app.fields["days_past_due"].delete(0, tk.END)
    desktop_app.fields["days_past_due"].insert(0, "90")
    desktop_app.fields["borrower_income"].delete(0, tk.END)
    desktop_app.fields["borrower_income"].insert(0, "55000")
    desktop_app.fields["prior_settlements"].delete(0, tk.END)
    desktop_app.fields["prior_settlements"].insert(0, "0")

    desktop_app._calculate()

    assert "$32,000.00" in desktop_app.amount_label.cget("text")
    assert "20.0%" in desktop_app.discount_label.cget("text")
    assert "6 months" in desktop_app.terms_label.cget("text")


def test_parse_float_rejects_invalid(desktop_app):
    desktop_app.fields["principal"].delete(0, tk.END)
    desktop_app.fields["principal"].insert(0, "not-a-number")
    with pytest.raises(ValueError, match="Original principal"):
        desktop_app._parse_float("principal", "Original principal")
