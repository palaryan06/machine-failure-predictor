@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
cd /d "%ROOT%"

if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo Run setup.bat first to create and install dependencies.
    exit /b 1
)

if not exist "python\dashboard\app.py" (
    echo [ERROR] Streamlit entry point not found: python\dashboard\app.py
    exit /b 1
)

set "PUBLISHER="
if exist "build\Debug\mqtt_demo.exe" set "PUBLISHER=build\Debug\mqtt_demo.exe"
if not defined PUBLISHER if exist "build\Release\mqtt_demo.exe" set "PUBLISHER=build\Release\mqtt_demo.exe"
if not defined PUBLISHER if exist "build\x64\Debug\mqtt_demo.exe" set "PUBLISHER=build\x64\Debug\mqtt_demo.exe"
if not defined PUBLISHER if exist "build\RelWithDebInfo\mqtt_demo.exe" set "PUBLISHER=build\RelWithDebInfo\mqtt_demo.exe"

if not defined PUBLISHER (
    echo [ERROR] mqtt_demo.exe was not found.
    echo Build the C++ publisher first from mqtt_c++ using CMake, then retry.
    exit /b 1
)

echo ============================================================
echo  Machine Failure Detection - Full Project Launch
echo ============================================================
echo.
echo [1/3] Starting Streamlit dashboard ...
start "MFD Dashboard" cmd /k ""%ROOT%run_dashboard.bat""

echo Waiting for dashboard to initialize ...
timeout /t 5 /nobreak >nul

echo [2/3] Starting C++ MQTT publisher ...
start "MFD Publisher" cmd /k ""%ROOT%run_publisher.bat""

echo Waiting before opening browser ...
timeout /t 3 /nobreak >nul

echo [3/3] Opening dashboard in default browser ...
start "" "http://localhost:8501"

echo.
echo ============================================================
echo [SUCCESS] Project launch started.
echo.
echo Dashboard window : MFD Dashboard
echo Publisher window : MFD Publisher
echo Browser URL      : http://localhost:8501
echo.
echo Open Live Monitoring in the dashboard to view incoming MQTT batches.
echo Close the dashboard and publisher windows to stop the system.
echo ============================================================
echo.

endlocal
exit /b 0
