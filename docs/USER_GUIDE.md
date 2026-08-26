# LegalAI — run and test on your PC

You do **not** need to be a programmer. You do **not** need Python for the test below.

## Do this now (about 2 minutes)

1. On your computer, open the LegalAI folder (the folder that contains `DOUBLE-CLICK-TO-TEST.bat`).
2. Double-click **`DOUBLE-CLICK-TO-TEST.bat`**.
3. Microsoft Edge or Chrome should open the calling desk.
4. Language is **हिन्दी** by default. Keep **Speak / बोलें** on to hear the agent.
5. Add numbers in bulk with **Import file**, **Import from link**, or **Paste numbers**.
6. Click **Start process / प्रक्रिया शुरू करें**, then OK.
7. Check **Ramesh Nair**: remaining **100000**, settlement **30000**, legal fee **5000**.
8. Click **Download Excel (CSV)** and open that file in Excel.

If the `.bat` file does nothing: open the `web` folder and double-click **`index.html`**.

If Windows says it blocked the file: right-click `DOUBLE-CLICK-TO-TEST.bat` → **Properties** → tick **Unblock** → **OK**, then double-click again.

## Add many numbers at once

- **Import file:** CSV or text. First row can be `name,phone` (or `mobile` / `number`).
- **Import from link:** paste an `https` CSV URL, or a Google Sheet link (use **File → Share → Publish to web** if the sheet is private). Best when the desk is opened via the app (`http://127.0.0.1:8000`), not only as a saved HTML file.
- **Paste numbers:** one line per person, `Name, 98765…` or only the phone.

Turn on **Replace list** if the file should wipe the current sheet instead of adding to it.

## Hindi speech

Choose **हिन्दी**. Tick **Speak / बोलें**. Windows Edge/Chrome usually includes an Indian Hindi voice. If you hear nothing, the transcript still shows Hindi; install a Hindi speech voice in Windows Settings → Time & language → Speech.

This is **Demo mode**. The AI agent speaks in the transcript box and fills the sheet. **Real phones do not ring.** That is the correct way to test the calling agent on your PC.

Example the firm asked for: remaining ₹1,00,000 → settle ₹30,000 → fee ₹5,000 (or ₹7,500 if they agree to 7.5%).

| Person | What you should see |
| --- | --- |
| Ramesh Nair | Interested, remaining 100000, settlement 30000, fee 5000 |
| Rahul Verma | No answer |
| Ananya Iyer | Not interested |
| Mohammed Irfan | No loan |
| Priya Sharma | Interested, amounts filled |

## Copy to another computer

Copy the whole folder. On the other PC, double-click `DOUBLE-CLICK-TO-TEST.bat` again. Or copy only the `web` folder and double-click `index.html`.

## Optional: Python window on Windows

Only if you already have Python 3.12 (tick **Add python.exe to PATH** when installing):

1. Double-click `windows\Install-LegalAI.bat`
2. Double-click `windows\Start-LegalAI.bat`

If Python is missing, those files now open the **same browser page** instead of failing.

## Real phone calls (next step)

Demo mode never rings a mobile. For a live call you need permission, TRAI/DND compliance, prepaid credit, a number that can dial India, and a Vapi account.

Natural Indian **woman** or **man** voice (not the robotic PC speaker): Azure neural Hindi Swara / Madhur via Vapi.

Plain-language checklist: [docs/LIVE_CALLING.md](LIVE_CALLING.md)

On the calling desk click **Live setup**, fill `.env` from `.env.example`, start with `windows\Start-LegalAI.bat` so the address is `http://127.0.0.1:8000`, tick **Live real call**, and test **one number you own**.

Demo mode does not call mobiles. Real ringing needs a Twilio account, money per minute, and numbers you are allowed to call. Use Demo mode until the sheet and transcript work. Then a technical person can put Twilio keys in the Python app **Settings**.

## If it still will not open

- Use **Edge** or **Chrome**, not Internet Explorer.
- Keep `web\index.html` inside the `web` folder.
- You can also ask someone to open `START-HERE.txt` and follow it with you.
