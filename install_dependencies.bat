@echo off
setlocal

:: Set the URL for the FFmpeg zip file
set "FFMPEG_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

:: Set the directory where FFmpeg will be installed
set "INSTALL_DIR=%USERPROFILE%\ffmpeg"

:: Set the name of the zip file
set "ZIP_FILE=%INSTALL_DIR%\ffmpeg.zip"

:: Create the installation directory
mkdir "%INSTALL_DIR%" 2>nul

:: Download FFmpeg
echo Downloading FFmpeg...
powershell -Command "Invoke-WebRequest -Uri '%FFMPEG_URL%' -OutFile '%ZIP_FILE%'"

:: Check if the download was successful
if not exist "%ZIP_FILE%" (
    echo Failed to download FFmpeg.
    pause
    exit /b 1
)

:: Extract FFmpeg
echo Extracting FFmpeg...
powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%INSTALL_DIR%' -Force"

:: Find the extracted FFmpeg directory
for /d %%D in ("%INSTALL_DIR%\ffmpeg-*") do set "FFMPEG_DIR=%%D"

:: Check if the extraction was successful
if not defined FFMPEG_DIR (
    echo Failed to extract FFmpeg.
    pause
    exit /b 1
)

:: Add FFmpeg's bin directory to the user's PATH
setx PATH "%FFMPEG_DIR%\bin;%PATH%"

echo FFmpeg has been installed and added to your PATH.
echo You may need to restart your command prompt or system for the changes to take effect.

pause