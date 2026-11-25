@echo off
setlocal
cd /d "%~dp0.."
py -3 run_all.py
if errorlevel 1 exit /b 1
py -3 -c "import sympy" >nul 2>nul
if not errorlevel 1 (
  py -3 symbolic_audit.py
  if errorlevel 1 exit /b 1
)
py -3 verify_manifest.py
if errorlevel 1 exit /b 1
pause
