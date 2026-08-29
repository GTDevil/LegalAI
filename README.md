# LegalAI — loan settlement calling desk

Excel-like sheet of names and numbers. **Start process** runs the AI agent and fills settlement (30% of remaining) and legal fee (5%–7.5%).

## Test on your PC right now (no Python)

1. Double-click **`DOUBLE-CLICK-TO-TEST.bat`**
2. Keep language **हिन्दी** and **Speak / बोलें** on
3. Add extra numbers with **Import file**, **Import from link**, or **Paste numbers**
4. Click **Start process**
5. Confirm **Ramesh Nair** shows remaining 100000, settlement 30000, fee 5000
6. Click **Download Excel (CSV)**

Or double-click `web/index.html` in Edge or Chrome.

Full staff steps: [docs/USER_GUIDE.md](docs/USER_GUIDE.md) and `START-HERE.txt`.

Demo mode does not ring real phones. For a live Indian-sounding call, see [docs/LIVE_CALLING.md](docs/LIVE_CALLING.md).

**Android APK:** [docs/ANDROID.md](docs/ANDROID.md) — Phone app calls, TeleCRM numbers/status, WhatsApp settlement messages. GitHub Action **Build Android APK**.

---

## Developers / Cursor Cloud

```bash
./.cursor/scripts/install.sh
.venv/bin/pytest -v
.venv/bin/python run_desktop.py --window
.venv/bin/python -m app.cli --input data/sample_leads.csv --output /tmp/leads-out.xlsx
.venv/bin/python run_web.py
```

Cursor skill: `.cursor/skills/loan-settlement-calling/SKILL.md`.

| Path | Role |
| --- | --- |
| `web/index.html` | No-install calling desk (double-click) |
| `DOUBLE-CLICK-TO-TEST.bat` | Opens that page on Windows |
| `app/desktop_ui.py` | Optional Tkinter window (`--window`) |
| `app/call_script.py` | Call script and demo conversations |
| `docs/USER_GUIDE.md` | Staff instructions |
