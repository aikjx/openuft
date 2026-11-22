$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
python src/root_v133.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python src/make_figures.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python src/property_audit.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Tests passed. For SHA-256 verification run sha256sum -c manifest.sha256, if supported."
