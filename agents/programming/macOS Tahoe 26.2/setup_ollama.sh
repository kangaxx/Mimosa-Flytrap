#!/usr/bin/env bash
set -euo pipefail

echo "==> Setup/Check Ollama on macOS"

if command -v ollama >/dev/null 2>&1; then
  echo "ollama is installed"
  ollama status || true
else
  echo "ollama not found. Attempting to install via Homebrew (if available)"
  if command -v brew >/dev/null 2>&1; then
    brew install ollama || true
    echo "After install, start the Ollama service with: ollama serve"
  else
    echo "Homebrew not available — please install Ollama manually: https://ollama.com/docs"
    exit 1
  fi
fi

echo "Configure models with: ollama pull <model-name>"
echo "Default base URL expected: http://localhost:11434"
