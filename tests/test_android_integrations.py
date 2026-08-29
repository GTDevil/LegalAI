"""Tests for TeleCRM payloads and WhatsApp settlement messages."""

from app.telecrm import lead_update_payload, leads_from_telecrm_json
from app.whatsapp_share import settlement_whatsapp_text, wa_digits, whatsapp_click_to_chat_url


def test_telecrm_payload_uses_name_phone_status():
    body = lead_update_payload(
        {
            "name": "Ramesh Nair",
            "phone": "9876501008",
            "call_status": "Completed",
            "settlement_amount": "30000.00",
            "notes": "Settle 30000",
        }
    )
    assert body["fields"]["Name"] == "Ramesh Nair"
    assert body["fields"]["Phone"] == "9876501008"
    assert body["fields"]["Status"] == "Completed"
    assert body["actions"][0]["type"] == "SYSTEM_NOTE"


def test_parse_telecrm_fields_wrapper():
    raw = {"data": [{"fields": {"Name": "Priya", "Phone": "9876543214"}}]}
    leads = leads_from_telecrm_json(raw)
    assert leads == [{"name": "Priya", "phone": "9876543214"}]


def test_whatsapp_one_lakh_hindi_message():
    text = settlement_whatsapp_text(name="Ramesh", remaining=100000, fee_percent=5, language="hi")
    assert "30000" in text.replace(",", "")
    assert "5000" in text.replace(",", "")
    assert "नमस्ते" in text
    url = whatsapp_click_to_chat_url("9876501008", text)
    assert url.startswith("https://wa.me/919876501008?text=")
    assert wa_digits("9876501008") == "919876501008"
