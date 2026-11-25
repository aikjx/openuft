@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 src\verify_v135.py
) else (
  python src\verify_v135.py
)
if errorlevel 1 (
  echo 验证失败，请检查 Python 安装与报错信息。
  exit /b 1
)
echo 验证执行结束。检查 data\verification_results.json 的运行范围和局限。
