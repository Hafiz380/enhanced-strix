<#
.SYNOPSIS
    Automated one-click installer for Enhanced Strix on Windows.
    Designed for non-technical users.
#>

$ErrorActionPreference = "Stop"
$STRIX_DIR = $PSScriptRoot

# 1. Visual Header
Clear-Host
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "   🦅 Enhanced Strix - Automated Setup 🦅   " -ForegroundColor White -BackgroundColor Blue
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Preparing your AI Pentesting environment..." -ForegroundColor Gray
Write-Host ""

# 2. System Checks
Write-Host "[1/5] Checking System Requirements..." -ForegroundColor Yellow

# Progress Bar
$progressParams = @{
    Activity = "Installing Enhanced Strix"
    Status = "Checking Python..."
    PercentComplete = 10
}
Write-Progress @progressParams

# Python Check
try {
    $pythonVersion = & py --version 2>$null
    if ($pythonVersion -match "3\.(1[2-9])") {
        Write-Host "  ✅ Python Found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python 3.12 or newer is required. Please install it from python.org."
    }
} catch {
    Write-Host "  ❌ Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.12+ from: https://www.python.org/downloads/" -ForegroundColor Gray
    Read-Host "Press Enter to exit..."
    exit
}

# Docker Check
Write-Progress -Activity "Installing Enhanced Strix" -Status "Checking Docker..." -PercentComplete 20
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "  ✅ Docker Found" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Docker not found. The tool will run, but sandbox features won't work." -ForegroundColor Yellow
}

# 3. Environment Setup
Write-Host ""
Write-Host "[2/5] Creating Private Environment (Virtual Env)..." -ForegroundColor Yellow
Write-Progress -Activity "Installing Enhanced Strix" -Status "Creating Virtual Environment..." -PercentComplete 40

if (-not (Test-Path "$STRIX_DIR\venv")) {
    & py -m venv venv
    Write-Host "  ✅ Environment Created" -ForegroundColor Green
} else {
    Write-Host "  ✅ Environment Already Exists" -ForegroundColor Green
}

# 4. Dependency Installation
Write-Host ""
Write-Host "[3/5] Installing Required Libraries (this may take 2 mins)..." -ForegroundColor Yellow
Write-Progress -Activity "Installing Enhanced Strix" -Status "Installing Libraries..." -PercentComplete 60

& "$STRIX_DIR\venv\Scripts\python.exe" -m pip install --upgrade pip | Out-Null
& "$STRIX_DIR\venv\Scripts\python.exe" -m pip install -e . | Out-Null

Write-Host "  ✅ All Libraries Installed" -ForegroundColor Green

# 5. Configuration Setup
Write-Host ""
Write-Host "[4/5] Preparing Configuration..." -ForegroundColor Yellow
Write-Progress -Activity "Installing Enhanced Strix" -Status "Configuring..." -PercentComplete 80

if (-not (Test-Path "$STRIX_DIR\.config")) {
    New-Item -ItemType Directory -Path "$STRIX_DIR\.config" -Force | Out-Null
}

Write-Host "  ✅ Configuration Ready" -ForegroundColor Green

# 6. Finalizing
Write-Host ""
Write-Host "[5/5] Creating Desktop Launchers..." -ForegroundColor Yellow
Write-Progress -Activity "Installing Enhanced Strix" -Status "Finalizing..." -PercentComplete 100

# Create Start Script
$launchContent = @"
@echo off
cd /d "%~dp0"
echo Starting Enhanced Strix Web Interface...
start http://localhost:8000
.\venv\Scripts\python.exe -m strix.interface.main web
pause
"@
$launchContent | Out-File -FilePath "$STRIX_DIR\Run_Strix_Web.bat" -Encoding ascii

Write-Host "  ✅ Desktop Launcher Created (Run_Strix_Web.bat)" -ForegroundColor Green

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "   🎉 INSTALLATION SUCCESSFUL! 🎉   " -ForegroundColor White -BackgroundColor DarkGreen
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor White
Write-Host "1. Double-click 'Run_Strix_Web.bat' in this folder." -ForegroundColor Gray
Write-Host "2. Go to 'Configuration' in the browser and add your API Key." -ForegroundColor Gray
Write-Host ""
Write-Host "Enjoy hacking safely!" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to finish..."
