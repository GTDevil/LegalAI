"""FastAPI application for the LegalAI Loan Settlement Agent."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.settlement import LoanCase, recommend_settlement

app = FastAPI(
    title="LegalAI Loan Settlement Agent",
    description="AI-assisted loan settlement recommendation API",
    version="0.1.0",
)


class SettlementRequest(BaseModel):
    principal: float = Field(gt=0, description="Original loan principal")
    outstanding_balance: float = Field(gt=0, description="Current outstanding balance")
    days_past_due: int = Field(ge=0, description="Days the loan is past due")
    borrower_income: float = Field(ge=0, description="Borrower's annual income")
    prior_settlements: int = Field(default=0, ge=0, description="Number of prior settlements")


class SettlementResponse(BaseModel):
    recommended_amount: float
    discount_percent: float
    payment_terms_months: int
    rationale: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "legalai-settlement-agent"}


@app.post("/api/v1/settlement/recommend", response_model=SettlementResponse)
def recommend(request: SettlementRequest) -> SettlementResponse:
    try:
        case = LoanCase(
            principal=request.principal,
            outstanding_balance=request.outstanding_balance,
            days_past_due=request.days_past_due,
            borrower_income=request.borrower_income,
            prior_settlements=request.prior_settlements,
        )
        offer = recommend_settlement(case)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SettlementResponse(
        recommended_amount=offer.recommended_amount,
        discount_percent=offer.discount_percent,
        payment_terms_months=offer.payment_terms_months,
        rationale=offer.rationale,
    )
