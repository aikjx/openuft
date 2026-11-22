$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$env:OPENBLAS_NUM_THREADS = "1"
py -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "test failure" }
if (Test-Path manifest.sha256) {
  Get-Content -Encoding UTF8 manifest.sha256 | ForEach-Object {
    if ($_.Trim()) {
      $parts = $_ -split '  ',2
      $actual = (Get-FileHash -Algorithm SHA256 $parts[1]).Hash.ToLowerInvariant()
      if ($actual -ne $parts[0]) { throw "SHA-256 mismatch: $($parts[1])" }
    }
  }
  Write-Output "SHA-256 manifest OK"
}
