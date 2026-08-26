"""HTTP API for settlement math and demo calling campaigns."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.call_agent import CampaignController
from app.call_script import simulate_call
from app.paths import project_root
from app.settings import AppSettings
from app.settlement import compute_settlement
from app.url_fetch import fetch_public_text, normalize_sheet_url
from app.workbook import Lead

app = FastAPI(
    title="LegalAI Loan Settlement Calling Agent",
    description="Spreadsheet-oriented loan settlement calling assistant",
    version="0.2.0",
)


class SettlementRequest(BaseModel):
    remaining_amount: float = Field(gt=0, description="Amount still owed")
    fee_percent: float = Field(default=7.5, description="Legal fee 5 to 7.5")
    settlement_percent: float = Field(default=30, description="At most 30% of remaining")


class SettlementResponse(BaseModel):
    remaining_amount: float
    settlement_amount: float
    fee_amount: float
    fee_percent: float
    settlement_percent: float
    summary: str


class SimulateCallRequest(BaseModel):
    name: str
    phone: str
    firm_name: str = "LegalAI Associates"


class CampaignLead(BaseModel):
    name: str = ""
    phone: str = ""


class CampaignRequest(BaseModel):
    leads: list[CampaignLead]
    firm_name: str = "LegalAI Associates"


class ImportUrlRequest(BaseModel):
    url: str = Field(min_length=8, description="https link to a CSV or Google Sheet")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "legalai-calling-agent"}


@app.get("/")
def calling_desk():
    page = project_root() / "web" / "index.html"
    if not page.exists():
        raise HTTPException(status_code=404, detail="Calling desk page is missing")
    return FileResponse(page)


@app.post("/api/v1/settlement/recommend", response_model=SettlementResponse)
def recommend(request: SettlementRequest) -> SettlementResponse:
    try:
        offer = compute_settlement(
            request.remaining_amount,
            fee_percent=request.fee_percent,
            settlement_percent=request.settlement_percent,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SettlementResponse(**offer.__dict__)


@app.post("/api/v1/calls/simulate")
def simulate(request: SimulateCallRequest) -> dict:
    result = simulate_call(Lead(name=request.name, phone=request.phone), firm_name=request.firm_name)
    lead = result.lead
    return {
        "outcome": result.outcome,
        "transcript": result.transcript,
        "lead": lead.display_values(),
    }


@app.post("/api/v1/import/from-url")
def import_from_url(request: ImportUrlRequest) -> dict:
    try:
        text = fetch_public_text(normalize_sheet_url(request.url))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not download that link") from exc
    return {"text": text}


@app.post("/api/v1/campaign/demo")
def demo_campaign(request: CampaignRequest) -> dict:
    leads = [Lead(name=item.name, phone=item.phone) for item in request.leads]
    settings = AppSettings(firm_name=request.firm_name, call_mode="demo", seconds_between_calls=0)
    report = CampaignController().run(leads, settings)
    return {
        "attempted": report.attempted,
        "completed": report.completed,
        "leads": [lead.display_values() for lead in leads],
    }
