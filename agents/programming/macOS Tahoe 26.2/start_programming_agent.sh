#!/usr/bin/env bash
set -euo pipefail

# Activates venv (if present) and starts the programming agent in interactive mode.
VENV=.venv
if [ -f "${VENV}/bin/activate" ]; then
  echo "Activating virtualenv ${VENV}"
  # shellcheck disable=SC1091
  source "${VENV}/bin/activate"
fi

echo "Starting programming agent (interactive). Use --auto for non-interactive runs."

# Find a usable python executable (prefer python then python3)
PY_CMD=""
if command -v python >/dev/null 2>&1; then
  PY_CMD=python
elif command -v python3 >/dev/null 2>&1; then
  PY_CMD=python3
else
  echo "Error: no python interpreter found. Install Python 3 (for example via Homebrew):"
  echo "  brew install python"
  exit 1
fi

"${PY_CMD}" run_programming_agent.py "$@"
