@echo off
chcp 65001 >NUL
cd /d "%~dp0"
python run_all.py
if errorlevel 1 (
 echo ROOT V87 tests failed. See output.
 exit /b 1
)
echo ROOT V87 verification completed. See results\verification_report.json
