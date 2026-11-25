@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 verify_v134.py
) else (
  python verify_v134.py
)
if errorlevel 1 (
  echo [FAIL] ROOT V134 mathematical audit failed.
  exit /b 1
)
echo [OK] All listed checks passed. Review limitations in the report.
exit /b 0
