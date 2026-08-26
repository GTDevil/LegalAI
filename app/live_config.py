"""Environment for real (live) phone calls. Never log secret values."""

from __future__ import annotations

import os


def vapi_api_key() -> str:
    return os.environ.get("VAPI_API_KEY", "").strip()


def vapi_phone_number_id() -> str:
    return os.environ.get("VAPI_PHONE_NUMBER_ID", "").strip()


def live_ready() -> bool:
    return bool(vapi_api_key() and vapi_phone_number_id())


def missing_live_settings() -> list[str]:
    missing: list[str] = []
    if not vapi_api_key():
        missing.append("VAPI_API_KEY")
    if not vapi_phone_number_id():
        missing.append("VAPI_PHONE_NUMBER_ID")
    return missing


REQUIREMENTS = [
    {
        "id": "consent",
        "title": "Permission to call",
        "detail": "Call only people your firm is allowed to contact. Follow TRAI / DND rules in India.",
    },
    {
        "id": "hours",
        "title": "Calling hours",
        "detail": "Outbound promotional/service calls in India are typically limited to permitted hours. Confirm current TRAI rules with your counsel.",
    },
    {
        "id": "identity",
        "title": "Identify the firm",
        "detail": "The agent must say the legal firm’s name and why it is calling.",
    },
    {
        "id": "number",
        "title": "A phone number that can call Indian mobiles",
        "detail": "Buy/rent a number in Vapi (or your telecom provider) that is allowed to dial +91.",
    },
    {
        "id": "vapi",
        "title": "Vapi account (recommended for a natural voice)",
        "detail": "Vapi places the real call and talks with a neural Indian voice. Create an account, add credits, and create a phone number.",
    },
    {
        "id": "voice",
        "title": "Indian woman or man voice",
        "detail": "We use Azure neural Hindi voices: Swara (woman) and Madhur (man). These sound much more natural than the browser demo voice.",
    },
    {
        "id": "money",
        "title": "Prepaid credit",
        "detail": "Each live minute costs money (telephony + voice + AI). Start with one test call to a phone you own.",
    },
    {
        "id": "server",
        "title": "Run the desk as a local app (not only a saved HTML file)",
        "detail": "Use Start-LegalAI.bat or: python run_web.py so the page is http://127.0.0.1:8000",
    },
]
