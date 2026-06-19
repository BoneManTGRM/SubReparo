@echo off
setlocal

set ROOT_DIR=%~dp0..
set TOOL_DIR=%ROOT_DIR%\tools\subreparo-immune

cd /d "%TOOL_DIR%"
python -m pip install -e .
if errorlevel 1 exit /b %errorlevel%

cd /d "%ROOT_DIR%"
echo Starting SubReparo Control Center...
echo Open: http://127.0.0.1:8765
subreparo-immune dashboard
