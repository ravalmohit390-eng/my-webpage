@echo off
REM ISODROP - Real-time Local Wi-Fi Data Sharing
REM Quick Start Script for Windows

echo.
echo ========================================
echo    ISODROP - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    pause
    exit /b 1
)

echo [OK] pip found
echo.

REM Install requirements
echo [*] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.

REM Start the server
echo [*] Starting ISODROP server...
echo.
python app.py
