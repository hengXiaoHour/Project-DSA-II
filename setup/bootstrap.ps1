param(
    [string]$RepoUrl = "https://github.com/hengXiaoHour/Project-DSA-II.git",
    [string]$Branch = "V2"
)

$ErrorActionPreference = "Stop"

# Step 1 — Check/install Python (handles Microsoft Store stub)
function Test-RealPython {
    $result = $false
    # Try py launcher first (more reliable on Windows)
    try { $null = py --version; $script:PyCmd = "py"; return $true } catch {}
    # Try python, but skip the Microsoft Store stub
    try {
        $ver = & python --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $ver -match "Python 3\.(1[3-9]|[2-9]\d)") {
            $script:PyCmd = "python"; return $true
        }
    } catch {}
    return $false
}

if (-not (Test-RealPython)) {
    Write-Host "Python 3 not found. Installing Python 3.13 via winget..." -ForegroundColor Yellow
    winget install --id Python.Python.3.13 -e --silent
    if ($LASTEXITCODE -ne 0) {
        Write-Host "winget failed. Install Python manually from https://python.org" -ForegroundColor Red
        exit 1
    }
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
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
