@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
cd /d "%ROOT%"

if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo Run setup.bat first to create and install dependencies.
    exit /b 1
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate the virtual environment.
    exit /b 1
)

if not exist "python\dashboard\app.py" (
    echo [ERROR] Streamlit entry point not found: python\dashboard\app.py
    exit /b 1
)

echo ============================================================
echo  Starting Streamlit Dashboard
echo ============================================================
echo Project root : %CD%
echo Entry point  : python\dashboard\app.py
echo URL          : http://localhost:8501
echo.
echo Press Ctrl+C in this window to stop the dashboard.
echo ============================================================
echo.

python -m streamlit run "python\dashboard\app.py"
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo.
    echo [ERROR] Streamlit exited with code %EXIT_CODE%.
)

endlocal
exit /b %EXIT_CODE%
