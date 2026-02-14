#!/usr/bin/env pwsh
Write-Host "==> Windows helper: check for winget and python"

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Warning "winget not found. Please install packages manually or install winget from Microsoft."
} else {
    Write-Host "winget found"
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Installing via winget..."
    winget install --accept-source-agreements --accept-package-agreements --id Python.Python.3 || Write-Warning "winget install failed. Install Python from https://python.org"
} else {
    Write-Host "Python detected"
}

Write-Host "Install completed (or verified). Next: run setup_environment.ps1"
