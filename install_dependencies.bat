@echo off
echo Installing required dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python from https://www.python.org/ and try again.
    pause
    exit /b 1
)

REM Ensure pip is installed
python -m ensurepip --upgrade >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install pip. Please check your Python installation.
    pause
    exit /b 1
)

REM Install yt_dlp and spotDL
echo Installing yt_dlp...
python -m pip install yt-dlp >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install yt_dlp.
    pause
    exit /b 1
)

echo Installing spotDL...
python -m pip install spotdl >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install spotDL.
    pause
    exit /b 1
)

echo All dependencies installed successfully.
pause