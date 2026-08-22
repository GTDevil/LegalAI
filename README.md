# LegalAI

Loan Settlement Agent — an AI-assisted API for recommending loan settlement offers based on borrower and loan factors.

## Development

### Setup

```bash
./.cursor/scripts/install.sh
```

### Run API server

```bash
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Run tests

```bash
.venv/bin/pytest -v
```

### API

- `GET /health` — health check
- `POST /api/v1/settlement/recommend` — get a settlement recommendation

Example request:

```bash
curl -X POST http://localhost:8000/api/v1/settlement/recommend \
  -H "Content-Type: application/json" \
  -d '{"principal": 50000, "outstanding_balance": 40000, "days_past_due": 90, "borrower_income": 55000}'
```
