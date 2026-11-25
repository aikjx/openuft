@echo off
cd /d "%~dp0"
py -3 run_all.py
if errorlevel 1 (echo FAIL & pause & exit /b 1)
echo Tests passed: mathematical consistency, NOT physical confirmation.
pause
