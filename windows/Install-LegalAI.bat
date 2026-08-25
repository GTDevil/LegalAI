@echo off
setlocal
cd /d "%~dp0\.."

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found.
  echo Install Python 3.12 from https://www.python.org/downloads/windows/
  echo Tick "Add python.exe to PATH" during setup, then run this file again.
  pause
  exit /b 1
)

echo Creating a private Python folder for LegalAI...
if not exist ".venv" python -m venv .venv

echo Installing the program (this needs internet, once)...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Install failed. Check the messages above.
  pause
  exit /b 1
)

echo.
echo Install finished. Next: double-click Start-LegalAI.bat
pause
