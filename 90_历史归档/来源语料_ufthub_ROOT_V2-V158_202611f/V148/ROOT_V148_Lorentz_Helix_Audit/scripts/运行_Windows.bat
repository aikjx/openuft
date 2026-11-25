@echo off
chcp 65001 >nul
cd /d "%~dp0.."
py -3 run_all.py
if errorlevel 1 exit /b 1
py -3 verify_manifest.py
if errorlevel 1 exit /b 1
pause
