@echo off
cd /d "%~dp0"
python -m unittest discover -s tests -v || exit /b 1
python experiments.py || exit /b 1
