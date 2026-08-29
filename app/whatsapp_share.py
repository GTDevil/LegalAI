"""WhatsApp message for a settlement customer (opens WhatsApp; the user taps Send)."""

from __future__ import annotations

from urllib.parse import quote

from app.settlement import compute_settlement


def wa_digits(phone: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    if len(digits) == 10:
        return "91" + digits
    if digits.startswith("91") and len(digits) >= 12:
        return digits
    return digits


def settlement_whatsapp_text(
    *,
    name: str,
    remaining: float,
    fee_percent: float = 7.5,
    firm_name: str = "LegalAI Associates",
    language: str = "hi",
) -> str:
    offer = compute_settlement(remaining, fee_percent=fee_percent)
    who = name.strip() or "ji"
    if language == "en":
        return (
            f"Hello {who}, this is {firm_name}. For remaining loan ₹{offer.remaining_amount:,.2f}, "
            f"we can work to settle at about ₹{offer.settlement_amount:,.2f} (within 30%) "
            f"and a legal fee of ₹{offer.fee_amount:,.2f} ({fee_percent:g}%). Please confirm if you wish to proceed."
        )
    return (
        f"नमस्ते {who}, {firm_name} से संपर्क है। बचे हुए लोन ₹{offer.remaining_amount:,.2f} पर "
        f"सेटलमेंट लगभग ₹{offer.settlement_amount:,.2f} (30% के भीतर) और कानूनी फीस ₹{offer.fee_amount:,.2f} "
        f"({fee_percent:g}%) है। अगर आगे बढ़ना हो तो कृपया पुष्टि करें।"
    )


def whatsapp_click_to_chat_url(phone: str, text: str) -> str:
    return f"https://wa.me/{wa_digits(phone)}?text={quote(text)}"
