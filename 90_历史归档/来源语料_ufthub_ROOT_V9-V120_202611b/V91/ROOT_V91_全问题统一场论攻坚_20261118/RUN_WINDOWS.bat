@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
 echo ERROR: Python 3.10+ not found in PATH
 exit /b 1
)
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
python run_all.py
exit /b %errorlevel%
