@echo off
cd /d "%~dp0"
python verify_checksums.py || exit /b 1
python run_all.py
pause
