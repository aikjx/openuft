@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (py -3 run_all.py) else (python run_all.py)
if errorlevel 1 (echo TEST FAILED & pause & exit /b 1)
echo All computational checks passed. This is NOT proof of a unified field theory.
pause
