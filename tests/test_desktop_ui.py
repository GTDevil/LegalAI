"""Tests for desktop UI helpers."""

import os
import tkinter as tk

import pytest

pytest.importorskip("tkinter")

if not os.environ.get("DISPLAY"):
    pytest.skip("Desktop UI tests need a display", allow_module_level=True)

from app.desktop_ui import LegalAIDesktopApp
from app.workbook import Lead


@pytest.fixture
def desktop_app():
    root = tk.Tk()
    root.withdraw()
    app = LegalAIDesktopApp(root)
    yield app
    root.destroy()


def test_sheet_loads_sample_rows(desktop_app):
    assert len(desktop_app.sheet.leads) >= 1
    assert any(lead.phone for lead in desktop_app.sheet.leads)


def test_add_person_updates_sheet(desktop_app):
    before = len(desktop_app.sheet.leads)
    desktop_app.sheet.leads.append(Lead(name="Test User", phone="9000000004"))
    desktop_app.sheet.reload()
    assert len(desktop_app.sheet.leads) == before + 1
    assert desktop_app.sheet.leads[-1].name == "Test User"
