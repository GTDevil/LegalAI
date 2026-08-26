"""Place a real outbound call with a neural Indian voice via Vapi."""

from __future__ import annotations

import httpx

from app.live_config import live_ready, missing_live_settings, vapi_api_key, vapi_phone_number_id

VAPI_CALLS_URL = "https://api.vapi.ai/call"
VOICE_WOMAN = "hi-IN-SwaraNeural"
VOICE_MAN = "hi-IN-MadhurNeural"


def normalize_e164(phone: str) -> str:
    trimmed = phone.strip().replace(" ", "").replace("-", "")
    if trimmed.startswith("+"):
        return trimmed
    digits = "".join(ch for ch in trimmed if ch.isdigit())
    if len(digits) == 10:
        return "+91" + digits
    if digits.startswith("91") and len(digits) == 12:
        return "+" + digits
    return "+" + digits if digits else trimmed


def azure_voice_id(gender: str, language: str) -> str:
    hindi = language != "en"
    woman = gender != "man"
    if hindi:
        return VOICE_WOMAN if woman else VOICE_MAN
    return "en-IN-NeerjaNeural" if woman else "en-IN-PrabhatNeural"


def settlement_system_prompt(firm_name: str, language: str) -> str:
    if language == "en":
        return (
            f"You are a polite caller from {firm_name}, a legal firm that helps people settle loans. "
            "Speak like a natural Indian woman or man on a phone call: short sentences, warm, not robotic. "
            "Ask if they have a loan with EMI trouble or already defaulted. If they want to settle, note total loan, "
            "remaining amount, and CIBIL or experience score. Offer to settle with the bank within 30% of remaining "
            "(example: remaining 1 lakh → about 30,000 or lesser) and a legal fee of 5% to 7.5% of remaining "
            "(5,000 or 7,500 on 1 lakh), whatever they are willing to pay. Do not threaten. Stop if they are not interested. "
            "If they share numbers, repeat them back to confirm."
        )
    return (
        f"आप {firm_name} से कॉल कर रही/रहे हैं। यह एक लीगल फर्म है जो लोन सेटलमेंट में मदद करती है। "
        "फोन पर एक सामान्य भारतीय महिला या पुरुष की तरह प्राकृतिक हिंदी में बात करें: छोटे वाक्य, विनम्र, बिना रोबोट जैसी आवाज़ के। "
        "पूछें कि क्या EMI भरने में दिक्कत है या लोन डिफॉल्ट हो चुका है। अगर सेटल करना चाहें तो कुल लोन, बचा हुआ बकाया, "
        "और CIBIL या अनुभव स्कोर नोट करें। बैंक से बचे हुए रकम के 30% के भीतर सेटल करवाने की बात करें "
        "(उदाहरण: 1 लाख बचा हो तो लगभग 30,000 या कम) और कानूनी फीस 5% से 7.5% "
        "(1 लाख पर 5,000 या 7,500), जो व्यक्ति देने को तैयार हो। धमकी न दें। ना करने पर विनम्रता से कॉल समाप्त करें।"
    )


def first_message(firm_name: str, person_name: str, language: str) -> str:
    who = person_name.strip() or "जी"
    if language == "en":
        return (
            f"Hello, am I speaking with {who}? I am calling on behalf of {firm_name}. "
            "Do you have a loan where EMIs are difficult, or has the loan already defaulted?"
        )
    return (
        f"नमस्ते, क्या मैं {who} से बात कर रहा हूँ? मैं {firm_name} की ओर से कॉल कर रहा हूँ। "
        "क्या आपके ऊपर ऐसा लोन है जिसकी EMI में दिक्कत है, या लोन डिफॉल्ट हो चुका है?"
    )


def place_vapi_call(
    *,
    name: str,
    phone: str,
    firm_name: str,
    voice_gender: str,
    language: str,
) -> dict:
    if not live_ready():
        raise RuntimeError(
            "Live calling is not ready. Missing: " + ", ".join(missing_live_settings())
        )
    voice_id = azure_voice_id(voice_gender, language)
    payload = {
        "phoneNumberId": vapi_phone_number_id(),
        "customer": {"number": normalize_e164(phone), "name": name or "Customer"},
        "assistant": {
            "firstMessage": first_message(firm_name, name, language),
            "model": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": settlement_system_prompt(firm_name, language)}
                ],
            },
            "voice": {"provider": "azure", "voiceId": voice_id},
            "transcriber": {
                "provider": "deepgram",
                "model": "nova-2",
                "language": "hi" if language != "en" else "en",
            },
        },
    }
    headers = {
        "Authorization": f"Bearer {vapi_api_key()}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=30.0) as client:
        response = client.post(VAPI_CALLS_URL, json=payload, headers=headers)
        try:
            body = response.json()
        except Exception:
            body = {"raw": response.text[:500]}
        if response.status_code >= 400:
            detail = body.get("message") or body.get("error") or body
            raise RuntimeError(f"Vapi did not place the call ({response.status_code}): {detail}")
    call_id = body.get("id") or body.get("callId") or ""
    return {
        "provider": "vapi",
        "call_id": str(call_id),
        "to": normalize_e164(phone),
        "voice_id": voice_id,
        "status": body.get("status") or "queued",
    }
