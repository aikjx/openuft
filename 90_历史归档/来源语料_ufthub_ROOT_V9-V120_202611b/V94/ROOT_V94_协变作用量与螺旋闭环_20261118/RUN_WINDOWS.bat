@echo off
cd /d "%~dp0"
python -m pip install -r requirements.txt
python verify_checksums.py
python run_all.py
pause
