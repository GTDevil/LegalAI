"""
LegalAI — real phone calls (before you switch anything on)

This is the next step after Demo mode. Demo never rings a real mobile.
A real call needs a phone company + a natural Indian voice service.
The browser “Speak / बोलें” voice is only for practice on your PC. It is not
good enough for a live customer call.

------------------------------------------------
What you must have BEFORE a live call
------------------------------------------------

1. Permission
   Call only people your firm is allowed to contact.
   In India this usually means TRAI / DND / preference-registry rules, and
   your lawyer should confirm Principal Entity / telemarketer registration
   if it applies to you.

2. Calling hours and identity
   The agent must say the firm name. Do not call at hours that are not allowed.

3. Money
   Live minutes cost money (phone network + AI voice + conversation model).
   Put prepaid credit on the accounts below. First call: a phone YOU own.

4. A number that can dial Indian mobiles (+91)
   Buy/rent this inside Vapi, or bring a number from an Indian CPaaS
   (Exotel, Knowlarity, etc.) if Vapi supports it.

5. A Vapi account (recommended)
   Vapi is what actually rings the phone and lets the AI talk both ways.
   Website: https://vapi.ai
   You will copy two values into a file named .env next to this project:
     VAPI_API_KEY=...
     VAPI_PHONE_NUMBER_ID=...

6. Run the desk as a small local website
   Double-click windows\Start-LegalAI.bat  (or: python run_web.py)
   Open http://127.0.0.1:8000
   A saved HTML file on the Desktop cannot place a real telecom call by itself.

7. Test on one number you own
   Do not start with the full client list.

------------------------------------------------
Natural Indian woman / man voice
------------------------------------------------

Demo mode uses the computer speaker. Live mode uses Azure neural Hindi:

  Woman:  hi-IN-SwaraNeural
  Man:    hi-IN-MadhurNeural

English (India) fallback: Neerja (woman) / Prabhat (man).

Pick Woman or Man on the calling desk under Live setup.
This is much closer to a real person than the demo voice.

------------------------------------------------
How to switch the desk to live
------------------------------------------------

1. Finish the list above.
2. Create a file named .env in the project folder (copy from .env.example).
3. Start the app so the address bar shows http://127.0.0.1:8000
4. Click Live setup. When it says Ready, tick Live real call.
5. Put ONE test number in the sheet. Start process. Your phone should ring.
6. After the call, type amounts into the sheet if the person shared them.
   (Auto-filling the Excel row from a live conversation is a later step.)

------------------------------------------------
What this is not
------------------------------------------------

- Not a bulk robocaller. Call people you are allowed to call.
- Not the same as the in-browser demo. Live needs accounts and credit.
- Old-style Twilio “robot read-aloud” is not used for this natural-voice path.
"""
