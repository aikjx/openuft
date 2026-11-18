@echo off
cd /d "%~dp0"
py -3 run_all.py --generate
if errorlevel 1 python run_all.py --generate
pause
