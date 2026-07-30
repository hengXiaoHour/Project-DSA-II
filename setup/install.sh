#!/usr/bin/env bash
set -e
echo "Setting up RUPP Campus Navigation..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "Done! Run: .venv/bin/python main.py"
