# LegalAI — loan settlement calling desk

Windows program for a legal firm that settles loans. It shows an **Excel-like sheet** of names and numbers. When you click **Start process**, an **AI agent** calls through the list and writes back interest, loan amounts, a **30% (or lesser) settlement offer**, and a **5%–7.5% legal fee**.

**Non-technical install, test, and copy-to-another-PC steps:** see [docs/USER_GUIDE.md](docs/USER_GUIDE.md).

---

## What you see after opening the app

- A sheet with Name, Phone, Call status, Interested, Total loan, Remaining, Settlement offered, Legal fee, CIBIL/experience, Notes
- **Start process** / **Stop**
- Open and save Excel (`.xlsx`) or CSV
- **Settings** (firm name, demo vs Twilio)

Example: remaining ₹1,00,000 → settlement ₹30,000 or lesser; fee ₹5,000 or ₹7,500.

Default mode is **Demo** (no real ringing). Use it to train staff. Live ringing needs Twilio credentials in Settings.

---

## Windows — no coding

1. GitHub **Actions** → **Build Windows EXE** → latest green run → download **LegalAI-windows-exe**
2. Unzip and double-click **LegalAI.exe**
3. Click **Start process**

Or copy this project folder to the PC, install Python 3.12 (tick **Add to PATH**), then:

1. `windows\Install-LegalAI.bat`
2. `windows\Start-LegalAI.bat`

---

## Developers / Cursor Cloud

```bash
./.cursor/scripts/install.sh
.venv/bin/pytest -v
.venv/bin/python run_desktop.py
.venv/bin/python -m app.cli --input data/sample_leads.csv --output /tmp/leads-out.xlsx
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
./scripts/build_exe.sh
```

Cursor skill: `.cursor/skills/loan-settlement-calling/SKILL.md`.

---

## Project layout

| Path | Role |
| --- | --- |
| `app/desktop_ui.py` | Excel-like calling desk |
| `app/call_script.py` | Call script and demo conversations |
| `app/call_agent.py` | Campaign runner (demo + Twilio) |
| `app/settlement.py` | 30% settlement and 5–7.5% fee |
| `app/workbook.py` | Load/save xlsx and csv |
| `data/sample_leads.csv` | Practice names and numbers |
| `docs/USER_GUIDE.md` | Staff instructions |
| `windows/*.bat` | Install and start on Windows |

---

## API (optional)

- `GET /health`
- `POST /api/v1/settlement/recommend` — `remaining_amount`, `fee_percent` (5–7.5), `settlement_percent` (≤30)
- `POST /api/v1/calls/simulate` — one demo call
- `POST /api/v1/campaign/demo` — demo campaign on a list of leads
