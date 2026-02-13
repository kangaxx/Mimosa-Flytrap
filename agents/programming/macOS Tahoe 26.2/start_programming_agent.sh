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
python run_programming_agent.py "$@"
