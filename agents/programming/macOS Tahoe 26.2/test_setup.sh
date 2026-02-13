#!/usr/bin/env bash
set -euo pipefail

echo "==> Basic sanity checks"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found"
  exit 1
fi

if [ -f .venv/bin/activate ]; then
  echo "Virtualenv present"
else
  echo "Virtualenv not found. Run ./setup_environment.sh"
fi

if command -v ollama >/dev/null 2>&1; then
  echo "ollama found"
else
  echo "ollama not found — ensure Ollama is installed and accessible"
fi

echo "Running minimal agent test (non-interactive)"
python run_langchain_agent.py --model-type ollama --prompt "Say hello"
