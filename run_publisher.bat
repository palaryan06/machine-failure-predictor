@echo off
setlocal EnableExtensions

set "ROOT=%~dp0"
cd /d "%ROOT%"

set "PUBLISHER="
if exist "build\Debug\mqtt_demo.exe" set "PUBLISHER=build\Debug\mqtt_demo.exe"
if not defined PUBLISHER if exist "build\Release\mqtt_demo.exe" set "PUBLISHER=build\Release\mqtt_demo.exe"
if not defined PUBLISHER if exist "build\x64\Debug\mqtt_demo.exe" set "PUBLISHER=build\x64\Debug\mqtt_demo.exe"
if not defined PUBLISHER if exist "build\RelWithDebInfo\mqtt_demo.exe" set "PUBLISHER=build\RelWithDebInfo\mqtt_demo.exe"

if not defined PUBLISHER (
    echo [ERROR] mqtt_demo.exe was not found.
    echo Build the C++ publisher first from mqtt_c++ using CMake, then retry.
    echo Checked:
    echo   build\Debug\mqtt_demo.exe
    echo   build\Release\mqtt_demo.exe
    echo   build\x64\Debug\mqtt_demo.exe
    echo   build\RelWithDebInfo\mqtt_demo.exe
    exit /b 1
)

for %%I in ("%PUBLISHER%") do set "PUBLISHER_DIR=%%~dpI"
for %%I in ("%PUBLISHER%") do set "PUBLISHER_EXE=%%~nxI"

echo ============================================================
echo  Starting C++ MQTT Publisher
echo ============================================================
echo Executable : %CD%\%PUBLISHER%
echo Working dir: %PUBLISHER_DIR%
echo.
echo Press Ctrl+C in this window to stop the publisher.
echo ============================================================
echo.

cd /d "%PUBLISHER_DIR%"
"%PUBLISHER_EXE%"
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo.
    echo [ERROR] Publisher exited with code %EXIT_CODE%.
)

endlocal
exit /b %EXIT_CODE%
