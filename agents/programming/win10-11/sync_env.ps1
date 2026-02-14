#!/usr/bin/env pwsh
Write-Host "Syncing .env from .env.example (windows)"
$example = ".env.example"
$target = ".env"

if ( -not (Test-Path $example) ) {
    Write-Error "$example not found in $(Get-Location)"
    exit 1
}

if ( -not (Test-Path $target) ) {
    Copy-Item $example $target
    Write-Host "Created $target from $example"
    exit 0
}

$backup = "$target.bak.$((Get-Date -UFormat %s))"
Copy-Item $target $backup
Write-Host "Backed up $target -> $backup"

$lines = Get-Content $example
foreach ($line in $lines) {
    if ($line.Trim().Length -eq 0 -or $line.Trim().StartsWith('#')) { continue }
    $parts = $line -split('=',2)
    if ($parts.Count -lt 2) { continue }
    $key = $parts[0]
    $val = $parts[1]
    $exists = Select-String -Path $target -Pattern "^$([regex]::Escape($key))=" -Quiet
    if ($exists) {
        if ($key -eq 'DEEPSEEK_MODEL') {
            (Get-Content $target) -replace "^$([regex]::Escape($key))=.*", "$key=$val" | Set-Content $target
            Write-Host "Updated $key in $target to example value"
        }
    } else {
        Add-Content -Path $target -Value $line
        Write-Host "Appended missing key $key to $target"
    }
}

Write-Host "Sync complete. Backup at $backup"
