@echo off
cd /d "%~dp0"
python run_all.py
if errorlevel 1 (
  echo ROOT V85 reproducibility failed. Check requirements and output.
  pause
  exit /b 1
)
echo ROOT V85 checks passed.
pause
