Write-Host "Setting up RUPP Campus Navigation..."
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
Write-Host "Done! Run: .venv\Scripts\python main.py"
