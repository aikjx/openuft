@echo off
setlocal
cd /d "%~dp0"
python -m unittest discover -s tests -v
if errorlevel 1 (echo FAILED & pause & exit /b 1)
python experiments\run.py
if errorlevel 1 (echo FAILED & pause & exit /b 1)
echo Tests and numerical data regeneration complete.
pause
