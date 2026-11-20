@echo off
setlocal
cd /d "%~dp0"
python run_all.py
if errorlevel 1 (
  echo ROOT V84 checks FAILED.
  exit /b 1
)
echo ROOT V84 checks PASSED. All observations are SYNTHETIC.
pause
