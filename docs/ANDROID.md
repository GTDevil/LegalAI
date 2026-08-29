# LegalAI on Android (APK)

This app is the same calling desk on a phone. It does **not** replace TeleCRM. It works **with** the Phone app, WhatsApp, and TeleCRM.

## What the APK does

1. **Call** — Opens your phone’s normal Phone / Dialer app with the number filled in. You tap Call. LegalAI is not a hidden auto-dialer.
2. **TeleCRM** — Pulls/pushes names, numbers, and status using **your** TeleCRM API token (from TeleCRM → Integrations → Website / API keys). You can also open the TeleCRM Play Store app (`app.telecrm.in`).
3. **WhatsApp** — Opens WhatsApp (or WhatsApp Business) with a ready Hindi/English settlement message. **You tap Send.** LegalAI does not send WhatsApp in the background.

## Install the APK

1. GitHub **Actions** → **Build Android APK** → latest green run → download **LegalAI-android-apk**.
2. On the phone: allow install from this source, open `app-debug.apk`.
3. First launch: demo sheet. Use **Call** on a test number you own.

This debug APK is for the firm’s own phones, not Play Store.

## TeleCRM setup (once)

1. Install [TeleCRM](https://play.google.com/store/apps/details?id=app.telecrm.in).
2. On telecrm.in: **Integrations → Website → API keys**. Create an **Async** token. Copy the **endpoint URL** and the **Bearer token** (shown once).
3. In LegalAI tap **TeleCRM setup**, paste URL + token, Save.
4. **Pull from TeleCRM** if your Sync/search URL is also pasted (optional). **Update TeleCRM** after a call to write status (Interested, remaining, settlement, fee).

Field names sent: Name, Phone, Status, Interested, Remaining amount, Settlement offered, Legal fee, Notes. Rename those fields in TeleCRM to match, or ask TeleCRM support if your workspace uses different labels.

## WhatsApp settlement message

Select a row that has remaining amount (or the demo will use remaining from the sheet). Tap **WhatsApp**. Check the text, then Send.

Example for ₹1,00,000 remaining at 5% fee: settlement ₹30,000, fee ₹5,000.

## Permissions

- Internet (TeleCRM API)
- Opening Phone and WhatsApp (no silent call, no silent WhatsApp)

Call only people the firm is allowed to contact. Follow TRAI/DND. WhatsApp messages only to customers who should receive them.
