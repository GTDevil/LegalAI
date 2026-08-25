# LegalAI — how to install, run, and test

This guide is written for people who are not programmers. You will use a Windows program that looks like Excel. An AI agent calls the people in the sheet and writes down whether they want loan settlement help.

## What the program does

1. You open the program.
2. You see a sheet with **Name** and **Phone**.
3. You click **Start process**.
4. The AI agent calls each person and asks if they have a loan they cannot pay EMIs for, or a loan that has already defaulted.
5. If the person wants to settle, the agent notes CIBIL (or experience) score and fills:
   - total loan amount
   - remaining loan amount
   - settlement amount offered (about **30% of remaining**, or lesser)
   - legal fee (**5% or 7.5%** of remaining, depending on what they agree to pay)
6. You can save the sheet as a normal Excel file.

Example: remaining amount ₹1,00,000 → settle for ₹30,000 or lesser; legal fee ₹5,000 or ₹7,500.

## Important: Demo mode vs real phone calls

**Demo mode (default, safe for training):** nobody’s real phone rings. The AI practices the conversation in the computer and still updates the sheet. Use this to learn the program and to test on any PC.

**Live Twilio mode:** real phones ring. You need a paid Twilio account, a Twilio phone number that is allowed to call India, and you must only call people your firm is legally allowed to contact. After a live call, type any amounts the person spoke into the sheet if they were not captured automatically.

## Option A — Easiest on Windows (no coding)

1. On GitHub, open **Actions**.
2. Open the workflow **Build Windows EXE**.
3. Open the latest run with a green tick.
4. Download the file **LegalAI-windows-exe**.
5. Unzip it. You should see **LegalAI.exe**.
6. Copy **LegalAI.exe** to the PC (Desktop is fine).
7. Double-click **LegalAI.exe**.
8. Click **Start process** and confirm.

If Windows says “Windows protected your PC”, choose **More info** → **Run anyway** (this happens with new unsigned programs).

## Option B — Install from this folder (Python on the PC)

Do this on each computer that should run the program.

### One-time setup on that computer

1. Install Python 3.12 from https://www.python.org/downloads/windows/
2. On the installer, tick **Add python.exe to PATH**.
3. Copy the whole LegalAI folder to the computer (USB, shared drive, or `git clone` if someone technical helps).
4. Double-click `windows\Install-LegalAI.bat`.
5. Wait until it says the install finished. If it asks for network permission, allow it.

### Every time you want to work

1. Double-click `windows\Start-LegalAI.bat`.
2. The calling desk window opens with the sheet.

## How to test (about 5 minutes)

Use **Demo mode** (the default). Sample people are already in the sheet.

| Person | Phone ending | What should happen |
| --- | --- | --- |
| Ramesh Nair | …08 | Interested — remaining ₹1,00,000, settlement ₹30,000, fee ₹5,000 |
| Rahul Verma | …10 | No answer |
| Ananya Iyer | …11 | Not interested |
| Mohammed Irfan | …13 | No loan |
| Priya Sharma | …14 | Interested — amounts and fee fill in |

1. Open the app.
2. Click **Start process** → **Yes**.
3. Watch the bottom **Call transcript**.
4. Check Priya’s row: Interested = Yes, settlement = 30% of remaining, legal fee 5% or 7.5%.
5. Click **Save sheet** and open the file in Microsoft Excel to confirm it looks right.

You can also double-click a cell to edit it, like Excel.

To test a new person: click **Add person**, use a 10-digit number ending in **4** (interested) or **0** (no answer), then Start process again. Rows already marked Completed / Not interested / No loan are skipped.

## Put it on another computer

- **With the .exe:** copy `LegalAI.exe` only. The sheet is saved under that Windows user’s AppData folder (`%APPDATA%\LegalAI\leads.xlsx`). To share results, use **Save sheet** and copy the Excel file.
- **With the folder:** copy the whole project folder, run `Install-LegalAI.bat` once on the new PC, then `Start-LegalAI.bat`.

## Turn on real phone calls (optional)

Only after Demo mode works.

1. Create a Twilio account and buy a calling number.
2. In the app, click **Settings**.
3. Set **Call mode** to `twilio`.
4. Paste Account SID, Auth Token, and From number.
5. Click **Save**.
6. Start with **one** test number you own.

Live calling costs money per minute. Follow TRAI / DND and your firm’s consent rules.

## If something goes wrong

| What you see | What to try |
| --- | --- |
| `python` is not recognized | Reinstall Python and tick Add to PATH, then open a new Command Prompt |
| Install bat flashes and closes | Right-click → Run with PowerShell, or run from Command Prompt to read the error |
| Sheet is empty | Click **Open Excel / CSV** and choose `data\sample_leads.csv` |
| Real calls fail | Switch call mode back to `demo`, check Twilio keys, check the From number can call the country |
| Excel will not open the file | Save as `.xlsx` not `.txt` |

A technical person can run tests with:

```text
.venv\Scripts\python -m pytest -v
.venv\Scripts\python -m app.cli --input data\sample_leads.csv --output %TEMP%\leads-out.xlsx
```
