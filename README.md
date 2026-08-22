# LegalAI

Loan Settlement Agent — desktop app and API for recommending loan settlement offers based on borrower and loan factors.

## Development

### Setup

```bash
./.cursor/scripts/install.sh
```

### Run desktop UI

```bash
.venv/bin/python run_desktop.py
```

### Run API server

```bash
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Run tests

```bash
.venv/bin/pytest -v
```

### Build standalone desktop executable

**On Windows (produces `LegalAI.exe` — double-click to open the desktop app):**

```bash
./scripts/build_exe.sh
```

**On Linux:**

```bash
./scripts/build_exe.sh
./dist/LegalAI
```

**API server executable** (optional, opens a background API instead of the desktop UI):

```bash
BUILD_TARGET=server ./scripts/build_exe.sh
```

**Download Windows `.exe` from GitHub:** open the repo’s **Actions** tab → **Build Windows EXE** → download the `LegalAI-windows-exe` artifact.

The desktop app lets you enter loan details, click **Calculate Settlement Offer**, and view the recommended amount, discount, payment terms, and rationale.

### API

- `GET /health` — health check
- `POST /api/v1/settlement/recommend` — get a settlement recommendation

Example request:

```bash
curl -X POST http://localhost:8000/api/v1/settlement/recommend \
  -H "Content-Type: application/json" \
  -d '{"principal": 50000, "outstanding_balance": 40000, "days_past_due": 90, "borrower_income": 55000}'
```
