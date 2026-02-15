@echo off
REM S. N. Joshi. Mess - Admin System Launcher
REM This script starts the Flask application on port 8080

echo.
echo =====================================================
echo   S. N. JOSHI. MESS - ADMIN MANAGEMENT SYSTEM
echo =====================================================
echo.

REM Verify database connection first
echo Verifying database connection...
python verify_setup.py > nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Database connection failed!
    echo Please ensure:
    echo   1. MySQL is running
    echo   2. track_serve database exists
    echo   3. Admin user is configured
    echo.
    pause
    exit /b 1
)

echo.
echo Starting Flask application on port 8080...
echo.
echo Access the application at: http://localhost:8080
echo.
echo Login Credentials:
echo   Phone: 7862017545
echo   Password: (Your admin password)
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py
