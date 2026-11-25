@echo off
cd /d "%~dp0"
python run_all.py || exit /b 1
python verify.py
