@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0\.."

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY where python3 >nul 2>nul && set "PY=python3"

if not defined PY (
  echo Python was not found. That is OK.
  echo Opening the browser version instead. No install needed.
  start "" "%cd%\web\index.html"
  pause
  exit /b 0
)

echo Creating a private Python folder for LegalAI...
if not exist ".venv" %PY% -m venv .venv
if not exist ".venv\Scripts\python.exe" (
  echo Could not create .venv. Opening the browser version instead.
  start "" "%cd%\web\index.html"
  pause
  exit /b 0
)

echo Installing the program (this needs internet, once)...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Install failed. Opening the browser version instead.
  start "" "%cd%\web\index.html"
  pause
  exit /b 0
)

echo.
echo Install finished.
echo Next you can double-click Start-LegalAI.bat  OR  DOUBLE-CLICK-TO-TEST.bat
pause
