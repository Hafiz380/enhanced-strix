@echo off
setlocal
cd /d "%~dp0"

echo --------------------------------------------------
echo      🦅 Enhanced Strix - One-Click Setup 🦅      
echo --------------------------------------------------
echo.
echo Preparing the installer... 
echo.

:: Check if PowerShell is available
where powershell >nul 2>nul
if %errorlevel% neq 0 (
    echo [Error] PowerShell is not found on this system.
    echo Please install Windows Management Framework or newer.
    pause
    exit /b 1
)

:: Run the PowerShell installer with elevated privileges if needed
powershell -ExecutionPolicy Bypass -File "setup.ps1"

if %errorlevel% neq 0 (
    echo.
    echo [Error] Installation failed. Please check the logs above.
    pause
    exit /b %errorlevel%
)

endlocal
exit /b 0
