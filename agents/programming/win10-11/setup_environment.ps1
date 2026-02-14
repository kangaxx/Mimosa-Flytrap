#!/usr/bin/env pwsh
Write-Host "==> Creating Python virtualenv and installing requirements"

$venv = ".venv"
if (-not (Test-Path $venv)) {
    python -m venv $venv
}

Write-Host "Activating virtualenv"
& .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host ".env created from .env.example — please edit with your API keys"
}

Write-Host "Environment ready. Activate with: .\\.venv\\Scripts\\Activate.ps1"
