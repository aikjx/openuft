@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -3 run_all.py
) else (
  python run_all.py
)
if errorlevel 1 (echo [FAIL] See errors & exit /b 1)
echo [PASS] Research checks and CSV/SVG files regenerated.
