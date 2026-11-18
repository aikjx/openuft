@echo off
cd /d "%~dp0"
python run_all.py
if errorlevel 1 exit /b 1
python experiments\generate.py
