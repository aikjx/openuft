@echo off
chcp 65001 >nul
cd /d "%~dp0"
python -m unittest discover -s tests -v
if errorlevel 1 exit /b 1
python experiments\run_experiments.py
if errorlevel 1 exit /b 1
start "" "web\index.html"
echo ROOT V63 math checks completed. Opened offline interactive lab.
pause
