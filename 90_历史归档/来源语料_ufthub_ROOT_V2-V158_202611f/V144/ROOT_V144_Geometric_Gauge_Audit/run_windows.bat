@echo off
setlocal
cd /d "%~dp0"
python run_all.py
if errorlevel 1 (
  echo [FAIL] ROOT V144 checks failed; install dependencies with python -m pip install -r requirements.txt
  exit /b 1
)
echo [PASS] ROOT V144 checks completed.
