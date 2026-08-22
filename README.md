# LegalAI

Loan Settlement Agent — a desktop app (and optional API) for recommending loan settlement offers.

---

## Start here (from scratch)

### If you only want the app on Windows (no coding)

1. Go to [GitHub Actions → Build Windows EXE](https://github.com/GTDevil/LegalAI/actions/workflows/build-windows-exe.yml)
2. Open the latest green checkmark run
3. Download artifact **`LegalAI-windows-exe`**
4. Extract **`LegalAI.exe`**
5. Double-click **`LegalAI.exe`**
6. Enter loan details → click **Calculate Settlement Offer**

### If you want to build on your PC (Windows)

```powershell
git clone https://github.com/GTDevil/LegalAI.git
cd LegalAI
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-build.txt
.venv\Scripts\python -m PyInstaller legalai-desktop.spec --noconfirm
```

Your app: `dist\LegalAI.exe`

### If you are developing in Cursor Cloud Agents

1. Save the environment in the Environment panel (install script: `./.cursor/scripts/install.sh`)
2. Start an agent on `GTDevil/LegalAI` / `main`
3. Run desktop UI: `.venv/bin/python run_desktop.py`
4. Run tests: `.venv/bin/pytest -v`

---

## Development commands

### Setup

```bash
./.cursor/scripts/install.sh
```

### Run desktop UI

```bash
.venv/bin/python run_desktop.py
```

### Run API server (optional)

```bash
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Run tests

```bash
.venv/bin/pytest -v
```

### Build desktop executable

```bash
./scripts/build_exe.sh
```

Output: `dist/LegalAI` (Linux) or `dist/LegalAI.exe` (Windows). No console window on Windows.

**API server executable** (optional):

```bash
BUILD_TARGET=server ./scripts/build_exe.sh
```

---

## Project layout

| Path | What it is |
| --- | --- |
| `app/desktop_ui.py` | Desktop window (Tkinter) |
| `app/settlement.py` | Settlement calculation logic |
| `app/main.py` | FastAPI API (optional) |
| `run_desktop.py` | Launch desktop app |
| `legalai-desktop.spec` | PyInstaller config for desktop `.exe` |
| `scripts/build_exe.sh` | One-command build script |

---

## API (optional)

- `GET /health`
- `POST /api/v1/settlement/recommend`

```bash
curl -X POST http://localhost:8000/api/v1/settlement/recommend \
  -H "Content-Type: application/json" \
  -d '{"principal": 50000, "outstanding_balance": 40000, "days_past_due": 90, "borrower_income": 55000}'
```
