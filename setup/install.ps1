Write-Host "Setting up RUPP Campus Navigation..."
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
Write-Host "Done! Run: .venv\Scripts\python main.py"
