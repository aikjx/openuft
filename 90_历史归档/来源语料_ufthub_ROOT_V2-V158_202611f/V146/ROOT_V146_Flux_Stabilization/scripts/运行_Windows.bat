@echo off
setlocal
cd /d "%~dp0.."
set PYTHONUTF8=1
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 run_all.py
) else (
  python run_all.py
)
if errorlevel 1 (
  echo ROOT V146 validation FAILED.
  pause
  exit /b 1
)
echo ROOT V146 validation completed.
pause
