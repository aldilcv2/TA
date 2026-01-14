#!/bin/bash

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Check if PyQt5 is installed, if not, try to install it (optional, mainly for first run convenience)
# python3 -c "import PyQt5" 2>/dev/null || pip3 install PyQt5

echo "Starting BiteBabe Admin Editor..."
python3 admin_editor.py
