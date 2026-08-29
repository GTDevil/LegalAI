"""Outbound call script and simulated borrower conversations.

The spoken process, kept in the firm's own words:

They get name and number of the person they are calling. Then they call them and
ask if they have loan which they are having trouble to pay EMIs for or already
they have defaulted the loan. If the person is willing to settle the loan, the
caller then checks their CIBIL score or experience score and a agreement with
the legal firm and the person is made that the firm will settle their loan with
the bank or with the entity they have taken loan from within 30% of the remaining
amount for which the legal firm will take a fee of 5 to 7.5%. That is, if the
loan is 1 lakh, the remaining amount is 1 lakh, the firm will settle it for
30,000 or lesser and take a charge of 5,000 or 7,500 depending on what the
person is willing to pay.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.settlement import choose_fee_percent, compute_settlement
from app.workbook import (
    STATUS_COMPLETED,
    STATUS_NO_ANSWER,
    STATUS_NO_LOAN,
    STATUS_NOT_INTERESTED,
    Lead,
)

OUTCOME_NO_ANSWER = "no_answer"
OUTCOME_NO_LOAN = "no_loan"
OUTCOME_NOT_INTERESTED = "not_interested"
OUTCOME_INTERESTED = "interested"


@dataclass
class CallResult:
    lead: Lead
    outcome: str
    transcript: list[str] = field(default_factory=list)


def greeting(firm_name: str, person_name: str) -> str:
    who = person_name.strip() or "there"
    return (
        f"Hello, am I speaking with {who}? I am calling on behalf of {firm_name}, "
        "a legal firm that helps people settle loans. Do you have a loan where you "
        "are having trouble paying EMIs, or have you already defaulted on the loan?"
    )


def settlement_explanation(remaining_amount: float, fee_percent: float, firm_name: str) -> str:
    offer = compute_settlement(remaining_amount, fee_percent=fee_percent)
    return (
        f"{firm_name} can work to settle this loan with the bank or lender within "
        f"30% of the remaining amount. For a remaining amount of ₹{remaining_amount:,.2f}, "
        f"that is about ₹{offer.settlement_amount:,.2f} or lesser. Our legal fee would be "
        f"₹{offer.fee_amount:,.2f} ({fee_percent:g}% of the remaining amount)."
    )


def twiml_say_script(firm_name: str, person_name: str) -> str:
    """Inline TwiML used when a live number is dialed without a media-stream AI."""
    spoken = (
        greeting(firm_name, person_name)
        + " If you are willing to settle, we will check your CIBIL or experience score "
        "and prepare an agreement. The firm will settle the remaining loan within 30 percent, "
        "and charge a legal fee of 5 to 7.5 percent. Please call us back if you wish to proceed. Thank you."
    )
    safe = (
        spoken.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    return f"<Response><Say voice=\"Polly.Aditi\" language=\"en-IN\">{safe}</Say></Response>"


def classify_demo_outcome(phone: str) -> str:
    """Stable demo outcomes so the same number always behaves the same way."""
    digits = "".join(ch for ch in phone if ch.isdigit())
    if not digits:
        return OUTCOME_NO_ANSWER
    last = int(digits[-1])
    if last == 0:
        return OUTCOME_NO_ANSWER
    if last in {1, 2}:
        return OUTCOME_NOT_INTERESTED
    if last == 3:
        return OUTCOME_NO_LOAN
    return OUTCOME_INTERESTED


def _amounts_from_phone(phone: str) -> tuple[float, float, str, bool]:
    digits = "".join(ch for ch in phone if ch.isdigit()) or "0"
    seed = int(digits[-4:]) if len(digits) >= 4 else int(digits)
    remaining = float(((seed % 9) + 1) * 100000)
    total = remaining + float((seed % 5) * 20000)
    cibil = 520 + (seed % 180)
    accepts_high_fee = int(digits[-1]) % 2 == 1
    return total, remaining, f"CIBIL {cibil}", accepts_high_fee


def simulate_call(lead: Lead, firm_name: str = "the legal firm") -> CallResult:
    """Run the settlement script against a simulated borrower and fill the lead."""
    transcript: list[str] = []
    name = lead.name.strip() or "the customer"
    transcript.append(f"AI: {greeting(firm_name, name)}")

    outcome = classify_demo_outcome(lead.phone)
    updated = Lead(**{**lead.__dict__})

    if outcome == OUTCOME_NO_ANSWER:
        transcript.append("System: The call was not answered.")
        updated.call_status = STATUS_NO_ANSWER
        updated.notes = "No answer"
        return CallResult(lead=updated, outcome=outcome, transcript=transcript)

    if outcome == OUTCOME_NO_LOAN:
        transcript.append(f"{name}: I do not have a loan like that.")
        transcript.append("AI: Thank you for your time. We will not proceed.")
        updated.call_status = STATUS_NO_LOAN
        updated.interested = "No"
        updated.notes = "Person said they do not have a troubled or defaulted loan"
        return CallResult(lead=updated, outcome=outcome, transcript=transcript)

    if outcome == OUTCOME_NOT_INTERESTED:
        transcript.append(f"{name}: I have a loan, but I am not interested in settlement.")
        transcript.append("AI: Understood. Thank you. You may contact us later if you change your mind.")
        updated.call_status = STATUS_NOT_INTERESTED
        updated.interested = "No"
        updated.notes = "Has a loan but declined settlement"
        return CallResult(lead=updated, outcome=outcome, transcript=transcript)

    total, remaining, score, accepts_high = _amounts_from_phone(lead.phone)
    fee_percent = choose_fee_percent(accepts_high)
    offer = compute_settlement(remaining, fee_percent=fee_percent)
    transcript.append(
        f"{name}: Yes. I am having trouble paying EMIs / the loan has defaulted. I am willing to settle."
    )
    transcript.append(
        "AI: Thank you. What is the total loan amount and the remaining amount, and may I note your "
        "CIBIL score or experience score?"
    )
    transcript.append(
        f"{name}: Total loan is ₹{total:,.0f}. Remaining is ₹{remaining:,.0f}. Score: {score}."
    )
    transcript.append(f"AI: {settlement_explanation(remaining, fee_percent, firm_name)}")
    if accepts_high:
        transcript.append(f"{name}: I agree to the {fee_percent:g}% legal fee and the settlement offer.")
    else:
        transcript.append(
            f"{name}: I can go ahead if the legal fee is {fee_percent:g}% rather than 7.5%."
        )
        transcript.append("AI: We can proceed at 5% as you are willing to pay that fee.")
    transcript.append(
        "AI: We will prepare an agreement that the firm will settle with the bank or lender "
        "within 30% of the remaining amount."
    )

    updated.call_status = STATUS_COMPLETED
    updated.interested = "Yes"
    updated.total_loan_amount = total
    updated.remaining_amount = remaining
    updated.settlement_amount = offer.settlement_amount
    updated.legal_fee = offer.fee_amount
    updated.fee_percent = offer.fee_percent
    updated.cibil_or_experience = score
    updated.notes = offer.summary
    return CallResult(lead=updated, outcome=OUTCOME_INTERESTED, transcript=transcript)
