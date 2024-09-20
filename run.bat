@echo off
:: Check for Admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process -File '%~f0' -Verb RunAs"
    exit /b
)

:: Set environment variables
set FLASK_APP=server.py
set FLASK_ENV=development

:: Create a temporary directory if it doesn't exist
set TEMP_DIR=C:\Temp\FlaskAudio
if not exist "%TEMP_DIR%" (
    mkdir "%TEMP_DIR%"
)

:: Set the temporary directory for audio files
set TMP="%TEMP_DIR%"
set TMPDIR="%TEMP_DIR%"
set TEMP="%TEMP_DIR%"

:: Change to the script directory
cd "C:\Users\Abhishek Patel\Documents\Work\Speech Recognition AI_Online\OBOT!!!"

:: Start the Flask app in a new minimized window
start /min cmd /c "python -m flask run"

:: Wait for a moment to ensure the server is running
timeout /t 5

:: Open the default web browser to the specified URL
start "" "http://127.0.0.1:5000"

exit
