@echo off
setlocal
cd /d "%~dp0\.."

if not exist ".venv\Scripts\python.exe" (
  echo LegalAI is not installed on this computer yet.
  echo Double-click Install-LegalAI.bat first.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" run_desktop.py
if errorlevel 1 (
  echo The program closed with an error. Screenshot this window and send it to your IT contact.
  pause
)
