"""Resolve bundled resources and writable user data folders."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def project_root() -> Path:
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return Path(meipass)
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def user_data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "LegalAI"
    else:
        base = Path.home() / ".legalai"
    base.mkdir(parents=True, exist_ok=True)
    return base


def sample_leads_path() -> Path:
    return project_root() / "data" / "sample_leads.csv"


def default_workbook_path() -> Path:
    return user_data_dir() / "leads.xlsx"


def settings_path() -> Path:
    return user_data_dir() / "settings.json"
