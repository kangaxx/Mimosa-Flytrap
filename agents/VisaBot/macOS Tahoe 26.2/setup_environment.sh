#!/usr/bin/env bash
set -euo pipefail

PYTHON=${PYTHON:-python3}
VENV_DIR=.venv

echo "==> Creating Python virtualenv in ${VENV_DIR}"
${PYTHON} -m venv ${VENV_DIR}
source ${VENV_DIR}/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  echo "Copying .env.example -> .env"
  cp .env.example .env
  echo "Edit .env to configure model backend and API keys"
fi

echo "Environment ready. Activate with: source ${VENV_DIR}/bin/activate"
