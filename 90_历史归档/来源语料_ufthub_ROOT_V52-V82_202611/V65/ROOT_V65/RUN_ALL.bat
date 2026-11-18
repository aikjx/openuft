@echo off
setlocal
cd /d "%~dp0"
echo === ROOT V65 new unit tests ===
python -m unittest discover -s tests -v || exit /b 1
echo === ROOT V64 patched legacy unit tests ===
pushd legacy_v64
python -m unittest discover -s tests -v
if errorlevel 1 (popd & exit /b 1)
popd
echo === regenerate model-only data ===
python experiments\generate.py || exit /b 1
echo Testing complete. G and four-force unification remain OPEN.
endlocal
