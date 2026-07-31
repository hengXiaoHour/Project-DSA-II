#!/usr/bin/env bash
set -e

echo "Setting up RUPP Campus Navigation..."

# Install prerequisites if missing (Debian/Ubuntu)
if ! command -v git >/dev/null 2>&1; then
    echo "Installing git..."
    sudo apt-get update && sudo apt-get install -y git
fi
if ! command -v python3 >/dev/null 2>&1; then
    echo "Installing python3..."
    sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip
fi
# Ensure venv module available
if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "Installing python3-venv..."
    sudo apt-get install -y python3-venv
fi

# Clone if not already cloned
if [ ! -d "Project-DSA-II" ]; then
    git clone https://github.com/hengXiaoHour/Project-DSA-II.git
    cd Project-DSA-II
else
    cd Project-DSA-II
fi

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
echo "Done! Run: .venv/bin/python main.py"
