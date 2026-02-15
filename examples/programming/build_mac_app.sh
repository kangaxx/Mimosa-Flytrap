#!/usr/bin/env bash
set -euo pipefail

# Simple macOS build script using PyInstaller.
# Produces a single-file windowed executable or .app bundle for the GUI demo.

HERE="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$HERE/.venv_build"
PYTHON=${PYTHON:-python3}

echo "Using python: $(command -v $PYTHON)"

if [ ! -x "$(command -v $PYTHON)" ]; then
  echo "Python not found: $PYTHON" >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtualenv in $VENV_DIR"
  "$PYTHON" -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install pyinstaller

cd "$HERE"

# Ensure demo files exist
if [ ! -f "gui_ollama_demo.py" ]; then
  echo "gui_ollama_demo.py not found in $HERE" >&2
  exit 1
fi

echo "Running PyInstaller..."
# windowed app (no console on macOS) and onefile
pyinstaller --noconfirm --windowed --onefile --name OllamaLocalDemo gui_ollama_demo.py --add-data "02_ollama_local_demo.py:."

echo "Build finished. Artifacts in $HERE/dist/ and $HERE/build/"
echo "If you need a .app bundle, inspect $HERE/dist/ (PyInstaller may produce OllamaLocalDemo.app or a single binary)."

deactivate || true

echo "Done."
