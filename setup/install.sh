#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Created virtual environment .venv/"
fi

source .venv/bin/activate 2>/dev/null || .venv/Scripts/activate 2>/dev/null

pip install -r setup/requirements.txt

playwright install chromium 2>/dev/null || python3 -m playwright install chromium 2>/dev/null || true

echo ""
echo "Setup complete. Run:"
echo "  .venv/bin/python main.py"
