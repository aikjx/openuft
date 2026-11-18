@echo off
cd /d "%~dp0"
python run_all.py
if errorlevel 1 exit /b 1
python experiments\run_analysis.py
if errorlevel 1 exit /b 1
python verify_package.py
