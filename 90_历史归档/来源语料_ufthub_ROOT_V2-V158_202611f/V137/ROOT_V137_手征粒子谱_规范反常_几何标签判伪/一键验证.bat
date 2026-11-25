@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3 src\verify_v137.py
if errorlevel 1 python src\verify_v137.py
if errorlevel 1 exit /b 1
pause
