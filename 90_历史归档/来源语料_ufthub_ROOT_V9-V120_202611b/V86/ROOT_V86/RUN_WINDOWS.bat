@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python 3.10 or later is needed.
  exit /b 1
)
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
python run_all.py --skip-browser
if errorlevel 1 exit /b 1
start "ROOT V86" "%~dp0web\index.html"
echo Audit passed. HTML opened in default browser.
endlocal
