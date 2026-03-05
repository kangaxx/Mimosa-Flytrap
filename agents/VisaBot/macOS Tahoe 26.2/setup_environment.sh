#!/usr/bin/env bash
set -euo pipefail

PYTHON=${PYTHON:-python3}
VENV_DIR=.venv

# Space-separated list of browsers to install: "chromium" (default), "firefox", "webkit", or "all".
PLAYWRIGHT_BROWSERS=${PLAYWRIGHT_BROWSERS:-chromium webkit}

echo "==> Creating Python virtualenv in ${VENV_DIR}"
if [ ! -d "${VENV_DIR}" ]; then
  ${PYTHON} -m venv ${VENV_DIR}
else
  echo "Virtualenv already exists — reusing ${VENV_DIR}"
fi
source ${VENV_DIR}/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ -f ./sync_env.sh ]; then
  bash ./sync_env.sh
else
  if [ ! -f .env ]; then
    echo "Copying .env.example -> .env"
    cp .env.example .env
    echo "Edit .env to configure model backend and API keys"
  fi
fi

echo "==> Installing Playwright browsers (${PLAYWRIGHT_BROWSERS})"
if [ "${PLAYWRIGHT_BROWSERS}" = "all" ]; then
  python -m playwright install
else
  # shellcheck disable=SC2086
  python -m playwright install ${PLAYWRIGHT_BROWSERS}
fi

echo "Environment ready. Activate with: source ${VENV_DIR}/bin/activate"
