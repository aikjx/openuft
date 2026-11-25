@echo off
cd /d "%~dp0"
where py >nul 2>&1 && (py -3 run_all.py & exit /b %errorlevel%)
python run_all.py
exit /b %errorlevel%
