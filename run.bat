@echo off
:: Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    goto admin
) else (
    echo Requesting Administrator privileges...
    PowerShell -Command "Start-Process '%~f0' -Verb RunAs"
    exit
)

:admin
echo Running BotBoy!!! with administrator privileges...

:: Navigate to the project directory
cd /d "C:\Users\Abhishek Patel\Documents\Work\Speech Recognition AI_Online\BotBoy!!!"

:: Check if server.py exists
if exist "server.py" (
    :: Run the server.py using Python in a new command window
    start cmd /c "python server.py"

    :: Wait a moment to allow the server to start
    timeout /t 5 /nobreak

    :: Open the default web browser to the BotBoy!!! page
    start "" "http://localhost:5000"
) else (
    echo server.py not found in the directory.
    pause
)

pause
