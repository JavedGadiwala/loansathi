@echo off
REM LoanSathi Personal - Windows Launcher
REM This script starts the Streamlit application

echo.
echo ========================================
echo LoanSathi Personal - Local Edition
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.12+ is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    echo Make sure to check 'Add Python to PATH' during installation
    pause
    exit /b 1
)

echo Starting LoanSathi Personal...
echo.

REM Install/upgrade dependencies if needed
echo Installing/updating dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo.
echo Launching application...
echo Opening browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

REM Start Streamlit app
streamlit run src/app.py --logger.level=info

pause
