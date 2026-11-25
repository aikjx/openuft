@echo off
setlocal
cd /d "%~dp0.."
py -3 -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
py -3 run_all.py
if errorlevel 1 exit /b 1
py -3 verify_manifest.py
if errorlevel 1 exit /b 1
pause
