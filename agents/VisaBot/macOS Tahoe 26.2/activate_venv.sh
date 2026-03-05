#!/usr/bin/env bash
# Usage: source ./activate_venv.sh

VENV_DIR=.venv

if [ ! -f "${VENV_DIR}/bin/activate" ]; then
  echo "Virtualenv not found at ${VENV_DIR}. Run ./setup_environment.sh first." >&2
  return 1 2>/dev/null || exit 1
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"
echo "Activated ${VENV_DIR} (python: $(command -v python))"

echo "Tip: run ./start_visabot.sh to start VisaBot"
