#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing macOS helper dependencies (Homebrew if available)"

if command -v brew >/dev/null 2>&1; then
  echo "Homebrew found — updating"
  brew update || true
  echo "Installing python@3.11 and curl"
  brew install python@3.11 curl || true
else
  echo "Homebrew not found. Please install Homebrew first: https://brew.sh/"
  exit 1
fi

echo "Done. Next: run ./setup_ollama.sh and ./setup_environment.sh"
