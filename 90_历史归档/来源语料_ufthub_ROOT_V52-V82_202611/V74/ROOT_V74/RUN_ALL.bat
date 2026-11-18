@echo off
cd /d "%~dp0"
python run_tests.py || exit /b 1
python symbolic_checks.py || exit /b 1
python run_experiments.py || exit /b 1
python build_catalog.py || exit /b 1
echo ROOT V74: all requested command-line checks passed.
