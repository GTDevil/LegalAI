#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

TARGET="${BUILD_TARGET:-desktop}"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv 2>/dev/null || python -m venv .venv
fi

if [[ -f .venv/Scripts/python.exe ]]; then
  PYTHON=".venv/Scripts/python.exe"
elif [[ -f .venv/bin/python ]]; then
  PYTHON=".venv/bin/python"
else
  echo "Could not find python in .venv"
  exit 1
fi

"$PYTHON" -m pip install --upgrade pip
"$PYTHON" -m pip install -r requirements-build.txt

rm -rf build dist

if [[ "$TARGET" == "server" ]]; then
  echo "Building API server executable..."
  "$PYTHON" -m PyInstaller legalai.spec --noconfirm
else
  echo "Building desktop UI executable..."
  "$PYTHON" -m PyInstaller legalai-desktop.spec --noconfirm
fi

echo ""
echo "Build complete ($TARGET)."
if [[ -f dist/LegalAI.exe ]]; then
  echo "Windows executable: dist/LegalAI.exe"
elif [[ -f dist/LegalAI ]]; then
  echo "Linux executable: dist/LegalAI"
else
  echo "Executable output is in dist/"
  ls -la dist/
fi
