---
name: loan-settlement-calling
description: Builds and maintains the LegalAI Windows calling desk for a loan-settlement legal firm. Use when working on the Excel-like leads sheet, AI outbound calls, CIBIL/settlement/fee fields, demo vs Twilio calling, or install/run guides for non-technical staff.
---

# Loan settlement calling agent

## When to use

Use this skill for LegalAI work involving:

- The on-screen Excel-like sheet of names and phone numbers
- The AI agent that calls those people and writes results back into the sheet
- Settlement at **30% of remaining** and legal fee **5% to 7.5%**
- Windows install, test, and run instructions for non-technical users

## Firm process (verbatim)

They get name and number of the person they are calling. Then they call them and ask if they have loan which they are having trouble to pay EMIs for or already they have defaulted the loan. If the person is willing to settle the loan, the caller then checks their CIBIL score or experience score and a agreement with the legal firm and the person is made that the firm will settle their loan with the bank or with the entity they have taken loan from within 30% of the remaining amount for which the legal firm will take a fee of 5 to 7.5%. That is, if the loan is 1 lakh, the remaining amount is 1 lakh, the firm will settle it for 30,000 or lesser and take a charge of 5,000 or 7,500 depending on what the person is willing to pay.

## Product the agent must preserve

Primary way staff run it on a PC: `web/index.html` / `DOUBLE-CLICK-TO-TEST.bat` (no Python).

Also keep:

- Tkinter window via `run_desktop.py --window`
- Demo AI filling the sheet after **Start process**
- Settlement at most 30% of remaining; fee 5–7.5%

Do not turn this back into a single-loan calculator screen as the main UI.

Windows staff: double-click `DOUBLE-CLICK-TO-TEST.bat` or open `web/index.html`. See `START-HERE.txt` and `docs/USER_GUIDE.md`.

## Numbers (do not invent new defaults)

| Item | Rule |
| --- | --- |
| Settlement offered | At most 30% of remaining amount (₹1,00,000 remaining → ₹30,000 or lesser) |
| Legal fee | 5% or 7.5% of remaining amount (₹5,000 or ₹7,500 on ₹1,00,000) |
| Currency | INR, Indian grouping |
| Live calls | Only when Settings `call_mode` is `twilio` and credentials exist |

Implementation: `app/settlement.py` (`compute_settlement`), `app/call_script.py` (script + demo borrower), `app/call_agent.py` (campaign), `app/workbook.py` (CSV/XLSX), `app/desktop_ui.py` (sheet UI).

## Demo phone endings (for testing without a carrier)

Last digit of the phone number:

- `0` — no answer
- `1` or `2` — has a loan, not interested
- `3` — no such loan
- `4`–`9` — interested; sheet fills amounts, 30% settlement, 5% or 7.5% fee, CIBIL

## Commands

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -v
.venv/bin/python run_desktop.py
.venv/bin/python -m app.cli --input data/sample_leads.csv --output /tmp/leads-out.xlsx
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Windows staff: double-click `DOUBLE-CLICK-TO-TEST.bat` or open `web/index.html`. See `START-HERE.txt` and `docs/USER_GUIDE.md`.

## Guardrails

- Call only numbers the firm is allowed to contact. Do not add autodial-until-answer, call blasting, or harassment retries.
- Do not log Twilio auth tokens into source control or README examples.
- Keep fee percent clamped to 5–7.5 and settlement percent at most 30.
- Live Twilio mode plays the script on the PSTN; full two-way voice-AI with automatic amount capture still needs a telephony+webhook product. Demo mode is what auto-fills the sheet end-to-end without a phone network.
