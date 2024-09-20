@echo off
SETLOCAL

REM Set the path to the FFmpeg bin directory
set "FFMPEG_DIR=C:\Users\Abhishek Patel\Documents\Work\Speech Recognition AI_Online\OBOT!!!\ffmpeg-2024-09-19-git-0d5b68c27c-full_build\bin"

REM Check if the directory exists
if not exist "%FFMPEG_DIR%" (
    echo FFmpeg directory not found!
    exit /b 1
)

REM Check if the FFmpeg executables exist
if not exist "%FFMPEG_DIR%\ffmpeg.exe" (
    echo ffmpeg.exe not found in %FFMPEG_DIR%!
    exit /b 1
)

if not exist "%FFMPEG_DIR%\ffplay.exe" (
    echo ffplay.exe not found in %FFMPEG_DIR%!
    exit /b 1
)

if not exist "%FFMPEG_DIR%\ffprobe.exe" (
    echo ffprobe.exe not found in %FFMPEG_DIR%!
    exit /b 1
)

REM Add FFmpeg to the PATH environment variable for the current session
set "PATH=%FFMPEG_DIR%;%PATH%"

REM Optional: Set PATH permanently (uncomment the line below)
REM setx PATH "%PATH%" /M

echo FFmpeg has been added to your PATH.
echo You can now use ffmpeg, ffplay, and ffprobe from any command prompt.

REM Verify the installation
ffmpeg -version
ffplay -version
ffprobe -version

echo Installation complete!
pause
ENDLOCAL
