param(
    [string]$RepoUrl = "https://github.com/hengXiaoHour/Project-DSA-II.git",
    [string]$Branch = "V2"
)

$ErrorActionPreference = "Stop"

# Step 1 — Ensure real Python is available
function Get-PythonCmd {
    try { $null = py --version; return "py" } catch {}
    try { $ver = & python --version 2>&1; if ($LASTEXITCODE -eq 0 -and $ver -match "Python 3") { return "python" } } catch {}
    return $null
}

$PyCmd = Get-PythonCmd
if (-not $PyCmd) {
    Write-Host "Python 3 not found. Installing Python 3.13 via winget..." -ForegroundColor Yellow
    winget install --id Python.Python.3.13 -e --silent
    if ($LASTEXITCODE -ne 0) {
        Write-Host "winget failed. Install Python manually from https://python.org" -ForegroundColor Red
        exit 1
    }
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
    $PyCmd = Get-PythonCmd
}
& $PyCmd --version

# Step 2 — Check/install Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found. Installing via winget..." -ForegroundColor Yellow
    winget install --id Git.Git -e --silent
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
}
git --version

# Step 2 — Clone
if (-not (Test-Path "Project-DSA-II")) {
    git clone $RepoUrl
}
cd Project-DSA-II
git checkout $Branch

# Step 3 — Setup venv + deps
Write-Host "Setting up RUPP Campus Navigation..." -ForegroundColor Yellow
& $PyCmd -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt

Write-Host "`nAll done! Run this to start:" -ForegroundColor Green
Write-Host ".venv\Scripts\python main.py" -ForegroundColor Cyan
