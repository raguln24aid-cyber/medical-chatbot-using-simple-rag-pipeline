# ============================================
# Research Agent - Auto Launcher Script
# ============================================

$backendDir = "c:\Users\RAGUL N\Desktop\research agent\backend"
$frontendDir = "c:\Users\RAGUL N\Desktop\research agent\frontend"
$venvDir = "$backendDir\.venv"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AI Research Assistant Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# --- STEP 1: Find a compatible Python (3.12 or 3.13 preferred) ---
Write-Host "`n[1/4] Looking for compatible Python (3.12 or 3.13)..." -ForegroundColor Yellow

$pythonExe = $null

# Try py launcher with specific versions first
foreach ($ver in @("3.13", "3.12", "3.11")) {
    try {
        $test = & py "-$ver" --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonExe = "py"
            $pyVersion = "-$ver"
            Write-Host "  Found Python $ver via py launcher" -ForegroundColor Green
            break
        }
    } catch {}
}

# If no specific version found, check default python version
if (-not $pythonExe) {
    try {
        $ver = & python --version 2>&1
        Write-Host "  Default python: $ver" -ForegroundColor Yellow
        if ($ver -match "3\.(8|9|10|11|12|13)") {
            $pythonExe = "python"
            $pyVersion = ""
            Write-Host "  Using default python (compatible)" -ForegroundColor Green
        } elseif ($ver -match "3\.14") {
            Write-Host "  WARNING: Python 3.14 detected - will use ABI3 compatibility workaround" -ForegroundColor Red
            $pythonExe = "python"
            $pyVersion = ""
            $useABI3 = $true
        }
    } catch {}
}

if (-not $pythonExe) {
    Write-Host "ERROR: No Python found. Please install Python 3.12 from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# --- STEP 2: Recreate venv if needed ---
Write-Host "`n[2/4] Setting up virtual environment..." -ForegroundColor Yellow

$needsRecreate = $false
if (Test-Path "$venvDir\Scripts\python.exe") {
    $venvPyVer = & "$venvDir\Scripts\python.exe" --version 2>&1
    Write-Host "  Existing venv Python: $venvPyVer" -ForegroundColor Gray
    if ($venvPyVer -match "3\.14") {
        Write-Host "  Venv uses Python 3.14 - will recreate with compatible version" -ForegroundColor Red
        $needsRecreate = $true
    }
} else {
    $needsRecreate = $true
}

if ($needsRecreate) {
    Write-Host "  Removing old venv..." -ForegroundColor Yellow
    if (Test-Path $venvDir) { Remove-Item -Recurse -Force $venvDir }
    
    Write-Host "  Creating new venv..." -ForegroundColor Yellow
    if ($pyVersion) {
        & py $pyVersion -m venv $venvDir
    } else {
        & python -m venv $venvDir
    }
    Write-Host "  Venv created successfully." -ForegroundColor Green
}

$pip = "$venvDir\Scripts\pip.exe"
$python = "$venvDir\Scripts\python.exe"

# --- STEP 3: Install requirements ---
Write-Host "`n[3/4] Installing backend dependencies (this may take a few minutes)..." -ForegroundColor Yellow

if ($useABI3) {
    Write-Host "  Using ABI3 forward compatibility mode for Python 3.14..." -ForegroundColor Yellow
    $env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY = "1"
}

& $pip install --upgrade pip -q
& $pip install -r "$backendDir\requirements.txt"

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nERROR: Failed to install dependencies." -ForegroundColor Red
    Write-Host "Please install Python 3.12 from https://www.python.org/downloads/release/python-3120/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "  All dependencies installed!" -ForegroundColor Green

# --- STEP 4: Launch servers ---
Write-Host "`n[4/4] Starting servers..." -ForegroundColor Yellow

# Start Backend
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Write-Host '=== BACKEND SERVER ===' -ForegroundColor Cyan; cd '$backendDir'; .\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"
) -WindowStyle Normal

Start-Sleep -Seconds 3

# Start Frontend
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Write-Host '=== FRONTEND SERVER ===' -ForegroundColor Green; cd '$frontendDir'; npm run dev"
) -WindowStyle Normal

Start-Sleep -Seconds 5

# Open browser
Write-Host "  Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:5173"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Servers are starting!" -ForegroundColor Green
Write-Host "  Backend  -> http://localhost:8000" -ForegroundColor White
Write-Host "  Frontend -> http://localhost:5173" -ForegroundColor White
Write-Host "  API Docs -> http://localhost:8000/docs" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan
Read-Host "Press Enter to close this launcher"
