@echo off
setlocal
cd /d "%~dp0\.."

if not exist ".venv\Scripts\python.exe" (
  echo Opening the calling desk in your browser. No extra install.
  start "" "%cd%\web\index.html"
  goto :eof
)

".venv\Scripts\python.exe" run_desktop.py
if errorlevel 1 (
  echo Opening the browser calling desk instead.
  start "" "%cd%\web\index.html"
)
