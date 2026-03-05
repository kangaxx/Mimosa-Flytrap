#!/usr/bin/env bash
set -euo pipefail

VENV=.venv
if [ -f "${VENV}/bin/activate" ]; then
  echo "Activating virtualenv ${VENV}"
  # shellcheck disable=SC1091
  source "${VENV}/bin/activate"
else
  echo "Virtualenv not found. Run ./setup_environment.sh first"
  exit 1
fi

PY_CMD=""
if command -v python >/dev/null 2>&1; then
  PY_CMD=python
elif command -v python3 >/dev/null 2>&1; then
  PY_CMD=python3
else
  echo "Error: no python interpreter found"
  exit 1
fi

"${PY_CMD}" run_visabot.py "$@"
