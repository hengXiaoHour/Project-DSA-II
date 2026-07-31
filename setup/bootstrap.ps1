param(
    [string]$RepoUrl = "https://github.com/hengXiaoHour/Project-DSA-II.git",
    [string]$Branch = "V2"
)

$ErrorActionPreference = "Stop"

# Step 1 — Check/install Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python not found. Installing via winget..." -ForegroundColor Yellow
    winget install --id Python.Python.3.13 -e --silent
    if ($LASTEXITCODE -ne 0) {
        Write-Host "winget failed. Install Python manually from https://python.org" -ForegroundColor Red
        exit 1
    }
}
# Refresh PATH
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
python --version

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
powershell -ExecutionPolicy Bypass -File setup\install.ps1

Write-Host "`nAll done! Run this to start:" -ForegroundColor Green
Write-Host ".venv\Scripts\python main.py" -ForegroundColor Cyan
