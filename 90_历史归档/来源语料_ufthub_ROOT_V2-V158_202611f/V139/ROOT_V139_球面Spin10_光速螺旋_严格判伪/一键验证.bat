@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 "src\verify_v139.py"
) else (
  python "src\verify_v139.py"
)
if errorlevel 1 (echo Verification FAILED & exit /b 1)
echo Verification PASSED. Output: data\verification_results.json
