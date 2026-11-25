@echo off
setlocal
chcp 65001 >NUL
cd /d "%~dp0"
where py >NUL 2>&1
if %errorlevel%==0 (
  py -3 src\verify_v136.py
) else (
  python src\verify_v136.py
)
if errorlevel 1 (
  echo [FAILED] V136 verification
  exit /b 1
)
python verify_archive.py
if errorlevel 1 exit /b 1
echo [PASS] ROOT V136 local verification
