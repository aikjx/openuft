@echo off
setlocal
cd /d "%~dp0.."
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (py -3 run_all.py) else (python run_all.py)
if errorlevel 1 (echo [FAIL] verification failed & exit /b 1)
echo [OK] verification passed
