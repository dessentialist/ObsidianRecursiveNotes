#!/bin/bash

# Determine the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    PY_VERSION=$(python --version 2>&1)
    if [[ $PY_VERSION == *"Python 3"* ]]; then
        PYTHON="python"
    else
        echo "Error: Python 3 is required but not found."
        exit 1
    fi
else
    echo "Error: Python 3 is required but not found."
    exit 1
fi

# Check if virtual environment exists and activate it if it does
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    if [ -f "venv/bin/activate" ]; then
        source "venv/bin/activate"
    elif [ -f "venv/Scripts/activate" ]; then
        source "venv/Scripts/activate"
    else
        echo "Warning: Virtual environment found but unable to activate it."
    fi
fi

# Run the GUI interface
echo "Starting Obsidian Recursive Notes Exporter..."
$PYTHON run.py

# Exit with the same code as the Python script
exit $? 