@echo off

echo Starting MQTT Subscriber...
start "Subscriber" cmd /k "cd /d %~dp0python\mqtt && python subscriber.py"

echo Starting MQTT Publisher...
start "Publisher" cmd /k "cd /d %~dp0build\Debug && mqtt_demo.exe"

echo All processes started.
pause