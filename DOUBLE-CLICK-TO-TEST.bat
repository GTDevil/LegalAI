@echo off
setlocal
cd /d "%~dp0"
echo.
echo LegalAI calling desk
echo Opening in your web browser. You do not need to install Python.
echo Click "Start process" on the page that opens.
echo.
if exist "web\index.html" (
  start "" "%~dp0web\index.html"
) else if exist "index.html" (
  start "" "%~dp0index.html"
) else (
  echo Could not find index.html
  pause
  exit /b 1
)
echo If a browser did not open, go to the web folder and double-click index.html
pause
