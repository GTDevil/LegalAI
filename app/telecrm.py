"""TeleCRM lead pull/push payloads. Token and URL come from the firm's TeleCRM API docs."""

from __future__ import annotations

from typing import Any


def lead_update_payload(lead: dict[str, Any], *, status: str | None = None) -> dict[str, Any]:
    """Body for TeleCRM async autoupdatelead (fields keyed as Name/Phone plus status)."""
    fields: dict[str, Any] = {
        "Name": lead.get("name") or "",
        "Phone": lead.get("phone") or "",
    }
    call_status = status or lead.get("call_status") or ""
    if call_status:
        fields["Status"] = call_status
    if lead.get("interested"):
        fields["Interested"] = lead["interested"]
    if lead.get("remaining_amount"):
        fields["Remaining amount"] = lead["remaining_amount"]
    if lead.get("settlement_amount"):
        fields["Settlement offered"] = lead["settlement_amount"]
    if lead.get("legal_fee"):
        fields["Legal fee"] = lead["legal_fee"]
    if lead.get("notes"):
        fields["Notes"] = lead["notes"]
    note = lead.get("notes") or call_status
    payload: dict[str, Any] = {"fields": fields}
    if note:
        payload["actions"] = [{"type": "SYSTEM_NOTE", "text": str(note)}]
    return payload


def leads_from_telecrm_json(raw: Any) -> list[dict[str, str]]:
    """Accept common TeleCRM / generic JSON list shapes."""
    rows: list[Any]
    if isinstance(raw, list):
        rows = raw
    elif isinstance(raw, dict):
        for key in ("leads", "data", "results", "items"):
            if isinstance(raw.get(key), list):
                rows = raw[key]
                break
        else:
            rows = [raw]
    else:
        return []

    leads: list[dict[str, str]] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        fields = item.get("fields") if isinstance(item.get("fields"), dict) else item
        lowered = {str(k).strip().lower(): v for k, v in fields.items()}
        name = str(lowered.get("name") or lowered.get("naam") or "")
        phone = str(
            lowered.get("phone")
            or lowered.get("mobile")
            or lowered.get("number")
            or lowered.get("phone number")
            or ""
        )
        if phone.strip():
            leads.append({"name": name.strip(), "phone": phone.strip()})
    return leads
