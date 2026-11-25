@echo off
cd /d "%~dp0\.."
py -3 -m pip install -r requirements.txt || exit /b 1
py -3 run_all.py || exit /b 1
py -3 verify_manifest.py
pause
