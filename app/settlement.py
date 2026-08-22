"""Rule-based loan settlement recommendation engine."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LoanCase:
    principal: float
    outstanding_balance: float
    days_past_due: int
    borrower_income: float
    prior_settlements: int = 0


@dataclass(frozen=True)
class SettlementOffer:
    recommended_amount: float
    discount_percent: float
    payment_terms_months: int
    rationale: str


def recommend_settlement(case: LoanCase) -> SettlementOffer:
    """Generate a settlement recommendation based on loan case factors."""
    if case.outstanding_balance <= 0:
        raise ValueError("Outstanding balance must be positive")
    if case.principal <= 0:
        raise ValueError("Principal must be positive")

    base_discount = 0.05
    if case.days_past_due >= 180:
        base_discount += 0.25
    elif case.days_past_due >= 90:
        base_discount += 0.15
    elif case.days_past_due >= 30:
        base_discount += 0.08

    if case.borrower_income < case.outstanding_balance * 0.1:
        base_discount += 0.10

    if case.prior_settlements > 0:
        base_discount -= 0.05 * case.prior_settlements

    discount = max(0.05, min(0.50, base_discount))
    recommended = round(case.outstanding_balance * (1 - discount), 2)

    if case.days_past_due >= 120:
        terms = 12
    elif case.days_past_due >= 60:
        terms = 6
    else:
        terms = 3

    rationale = (
        f"Recommended {discount:.0%} discount on ${case.outstanding_balance:,.2f} balance "
        f"({case.days_past_due} days past due, income ${case.borrower_income:,.2f})."
    )

    return SettlementOffer(
        recommended_amount=recommended,
        discount_percent=round(discount * 100, 1),
        payment_terms_months=terms,
        rationale=rationale,
    )
