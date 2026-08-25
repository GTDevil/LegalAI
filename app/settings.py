"""Saved application settings (firm name, call mode, optional Twilio keys)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from app.paths import settings_path
from app.settlement import DEFAULT_SETTLEMENT_PERCENT, FEE_PERCENT_HIGH, FEE_PERCENT_LOW


@dataclass
class AppSettings:
    firm_name: str = "LegalAI Associates"
    settlement_percent: float = DEFAULT_SETTLEMENT_PERCENT
    fee_percent_low: float = FEE_PERCENT_LOW
    fee_percent_high: float = FEE_PERCENT_HIGH
    call_mode: str = "demo"
    seconds_between_calls: float = 1.0
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_from_number: str = ""


def load_settings(path: Path | None = None) -> AppSettings:
    file_path = path or settings_path()
    if not file_path.exists():
        return AppSettings()
    raw = json.loads(file_path.read_text(encoding="utf-8"))
    allowed = {key: raw[key] for key in AppSettings.__dataclass_fields__ if key in raw}
    return AppSettings(**allowed)


def save_settings(settings: AppSettings, path: Path | None = None) -> None:
    file_path = path or settings_path()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")
