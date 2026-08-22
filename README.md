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

### Build standalone executable

**On Windows (produces `LegalAI.exe`):**

```bash
./scripts/build_exe.sh
```

The output is `dist/LegalAI.exe`. Double-click it or run from Command Prompt:

```bash
dist\LegalAI.exe --open-browser
```

**On Linux (produces `dist/LegalAI`):**

```bash
./scripts/build_exe.sh
./dist/LegalAI --host 127.0.0.1 --port 8000
```

**Download Windows `.exe` from GitHub:** after pushing to `main`, open the repo’s **Actions** tab → **Build Windows EXE** → download the `LegalAI-windows-exe` artifact.

Options:

- `--host` — bind address (default `127.0.0.1`)
- `--port` — port (default `8000`)
- `--open-browser` — open API docs in your browser

### API

- `GET /health` — health check
- `POST /api/v1/settlement/recommend` — get a settlement recommendation

Example request:

```bash
curl -X POST http://localhost:8000/api/v1/settlement/recommend \
  -H "Content-Type: application/json" \
  -d '{"principal": 50000, "outstanding_balance": 40000, "days_past_due": 90, "borrower_income": 55000}'
```
