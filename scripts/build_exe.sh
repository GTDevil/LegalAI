#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements-build.txt

rm -rf build dist
.venv/bin/pyinstaller legalai.spec --noconfirm

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
