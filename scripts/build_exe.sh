#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -d .venv ]]; then
  python3 -m venv .venv 2>/dev/null || python -m venv .venv
fi

if [[ -f .venv/Scripts/pip.exe ]]; then
  PIP=".venv/Scripts/pip.exe"
  PYINSTALLER=".venv/Scripts/pyinstaller.exe"
elif [[ -f .venv/bin/pip ]]; then
  PIP=".venv/bin/pip"
  PYINSTALLER=".venv/bin/pyinstaller"
else
  echo "Could not find pip in .venv"
  exit 1
fi

"$PIP" install --upgrade pip
"$PIP" install -r requirements-build.txt

rm -rf build dist
"$PYINSTALLER" legalai.spec --noconfirm

echo ""
echo "Build complete."
if [[ -f dist/LegalAI.exe ]]; then
  echo "Windows executable: dist/LegalAI.exe"
elif [[ -f dist/LegalAI ]]; then
  echo "Linux executable: dist/LegalAI"
else
  echo "Executable output is in dist/"
  ls -la dist/
fi
