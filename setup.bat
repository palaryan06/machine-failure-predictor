@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
cd /d "%ROOT%"

echo ============================================================
echo  Machine Failure Detection - Environment Setup
echo ============================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found in PATH.
    echo Install Python 3.10+ and ensure "python" is available.
    exit /b 1
)

for /f "delims=" %%V in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set "PY_VERSION=%%V"
echo Detected Python %PY_VERSION%

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo Creating virtual environment in .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create the virtual environment.
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment ...
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate the virtual environment.
    exit /b 1
)

echo.
echo Upgrading pip ...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip.
    exit /b 1
)

echo.
echo Installing dependencies from requirements.txt ...
python -m pip install -r "requirements.txt"
if errorlevel 1 (
    echo [ERROR] Dependency installation failed.
    exit /b 1
)

echo.
echo ============================================================
echo [SUCCESS] Setup complete.
echo.
echo Next steps:
echo   run_dashboard.bat  - Launch the Streamlit dashboard
echo   run_publisher.bat  - Launch the C++ MQTT publisher
echo   run_project.bat    - Launch dashboard + publisher together
echo ============================================================
echo.

endlocal
exit /b 0
