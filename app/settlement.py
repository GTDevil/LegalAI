"""Loan settlement offer and legal-fee calculations.

Business rule: the firm offers to settle remaining dues at up to 30% of the
remaining amount, and charges a legal fee of 5% to 7.5% of the remaining amount.
Example: remaining ₹1,00,000 → settlement ₹30,000 or lesser; fee ₹5,000 or ₹7,500.
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_SETTLEMENT_PERCENT = 30.0
FEE_PERCENT_LOW = 5.0
FEE_PERCENT_HIGH = 7.5


@dataclass(frozen=True)
class SettlementOffer:
    remaining_amount: float
    settlement_amount: float
    fee_amount: float
    fee_percent: float
    settlement_percent: float
    summary: str


def _require_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def compute_settlement(
    remaining_amount: float,
    *,
    fee_percent: float = FEE_PERCENT_HIGH,
    settlement_percent: float = DEFAULT_SETTLEMENT_PERCENT,
) -> SettlementOffer:
    """Compute settlement (≤ 30% of remaining) and legal fee (5%–7.5%)."""
    _require_positive("Remaining amount", remaining_amount)

    if settlement_percent <= 0 or settlement_percent > DEFAULT_SETTLEMENT_PERCENT:
        raise ValueError("Settlement percent must be greater than 0 and at most 30")
    if fee_percent < FEE_PERCENT_LOW or fee_percent > FEE_PERCENT_HIGH:
        raise ValueError("Fee percent must be between 5 and 7.5")

    settlement_amount = round(remaining_amount * (settlement_percent / 100.0), 2)
    fee_amount = round(remaining_amount * (fee_percent / 100.0), 2)
    summary = (
        f"Settle ₹{settlement_amount:,.2f} ({settlement_percent:g}% of remaining "
        f"₹{remaining_amount:,.2f}). Legal fee ₹{fee_amount:,.2f} ({fee_percent:g}%)."
    )
    return SettlementOffer(
        remaining_amount=round(remaining_amount, 2),
        settlement_amount=settlement_amount,
        fee_amount=fee_amount,
        fee_percent=fee_percent,
        settlement_percent=settlement_percent,
        summary=summary,
    )


def choose_fee_percent(borrower_accepts_high_fee: bool) -> float:
    """7.5% if the person agrees to the standard fee, otherwise 5%."""
    return FEE_PERCENT_HIGH if borrower_accepts_high_fee else FEE_PERCENT_LOW


def format_inr(amount: float | None) -> str:
    if amount is None:
        return ""
    negative = amount < 0
    value = abs(float(amount))
    whole, frac = f"{value:.2f}".split(".")
    if len(whole) <= 3:
        grouped = whole
    else:
        last3 = whole[-3:]
        rest = whole[:-3]
        parts: list[str] = []
        while len(rest) > 2:
            parts.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.append(rest)
        grouped = ",".join(reversed(parts)) + "," + last3
    sign = "-" if negative else ""
    return f"₹{sign}{grouped}.{frac}"
