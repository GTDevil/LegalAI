"""Run calling campaigns: demo AI conversations, or live Twilio dials."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from dataclasses import dataclass

from app.call_script import simulate_call, twiml_say_script
from app.settings import AppSettings
from app.workbook import (
    STATUS_CALLING,
    STATUS_COMPLETED,
    STATUS_FAILED,
    STATUS_NO_LOAN,
    STATUS_NOT_CALLED,
    STATUS_NOT_INTERESTED,
    Lead,
)

TERMINAL_STATUSES = {
    STATUS_COMPLETED,
    STATUS_NOT_INTERESTED,
    STATUS_NO_LOAN,
    "Live call placed",
}

ProgressCallback = Callable[[int, Lead, list[str]], None]


@dataclass
class CampaignReport:
    attempted: int = 0
    completed: int = 0
    skipped: int = 0


class CampaignController:
    def __init__(self) -> None:
        self._stop = threading.Event()
        self._running = threading.Event()

    def request_stop(self) -> None:
        self._stop.set()

    def running(self) -> bool:
        return self._running.is_set()

    def run(
        self,
        leads: list[Lead],
        settings: AppSettings,
        on_progress: ProgressCallback | None = None,
    ) -> CampaignReport:
        self._stop.clear()
        self._running.set()
        report = CampaignReport()
        try:
            for index, lead in enumerate(leads):
                if self._stop.is_set():
                    break
                if not lead.phone.strip() or lead.call_status in TERMINAL_STATUSES:
                    report.skipped += 1
                    continue

                lead.call_status = STATUS_CALLING
                if on_progress:
                    on_progress(index, lead, [f"System: Dialing {lead.phone}…"])

                try:
                    if settings.call_mode == "twilio":
                        transcript = place_twilio_call(lead, settings)
                        lead.notes = (lead.notes + " " if lead.notes else "") + "Live call placed via Twilio."
                        lead.call_status = "Live call placed"
                        result_lead = lead
                    else:
                        result = simulate_call(lead, firm_name=settings.firm_name)
                        result_lead = result.lead
                        transcript = result.transcript
                    report.attempted += 1
                    report.completed += 1
                    leads[index] = result_lead
                    if on_progress:
                        on_progress(index, result_lead, transcript)
                except Exception as exc:  # noqa: BLE001 - surface any provider error on the row
                    lead.call_status = STATUS_FAILED
                    lead.notes = str(exc)
                    report.attempted += 1
                    if on_progress:
                        on_progress(index, lead, [f"System: Call failed — {exc}"])

                if settings.seconds_between_calls > 0 and not self._stop.is_set():
                    time.sleep(settings.seconds_between_calls)
        finally:
            self._running.clear()
        return report


def pending_indices(leads: list[Lead]) -> list[int]:
    ready: list[int] = []
    for index, lead in enumerate(leads):
        if not lead.phone.strip():
            continue
        if lead.call_status in {STATUS_NOT_CALLED, STATUS_FAILED, "No answer"}:
            ready.append(index)
    return ready


def place_twilio_call(lead: Lead, settings: AppSettings) -> list[str]:
    if not settings.twilio_account_sid or not settings.twilio_auth_token or not settings.twilio_from_number:
        raise RuntimeError(
            "Live calling is not configured. Open Settings and add Twilio Account SID, Auth Token, and From number."
        )
    try:
        from twilio.rest import Client
    except ImportError as exc:
        raise RuntimeError("The Twilio library is not installed. Re-run the installer.") from exc

    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    twiml = twiml_say_script(settings.firm_name, lead.name)
    call = client.calls.create(
        to=_normalize_phone(lead.phone),
        from_=settings.twilio_from_number,
        twiml=twiml,
    )
    return [
        f"System: Live call started (Twilio SID {call.sid}).",
        "AI: Playing the settlement script on the phone.",
        "System: After a live call, type the person's answers into the sheet if they shared amounts.",
    ]


def _normalize_phone(phone: str) -> str:
    trimmed = phone.strip().replace(" ", "").replace("-", "")
    if trimmed.startswith("+"):
        return trimmed
    digits = "".join(ch for ch in trimmed if ch.isdigit())
    if len(digits) == 10:
        return "+91" + digits
    return "+" + digits
