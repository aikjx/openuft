$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python src/root_v134.py | Out-Null
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python src/property_audit.py | Out-Null
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python src/make_figures.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Get-Content -LiteralPath manifest.sha256 | ForEach-Object {
    $parts = $_ -split '  ',2
    $sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $parts[1]).Hash.ToLower()
    if ($sha -ne $parts[0]) { throw "Checksum mismatch: $($parts[1])" }
}
Write-Host 'SHA-256 manifest verified'
