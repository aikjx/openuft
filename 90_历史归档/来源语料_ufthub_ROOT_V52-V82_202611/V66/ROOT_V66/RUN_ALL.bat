@echo off
cd /d "%~dp0"
py -3 run_all.py
if errorlevel 1 exit /b 1
py -3 experiments\generate.py
pause
