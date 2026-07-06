#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Determine Python executable
if [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
elif [ -f ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
else
    PYTHON="python3"
fi

# Install dependencies
echo "Installing dependencies..."
$PYTHON -m pip install -q -r requirements.txt

# Run tests
$PYTHON -m pytest --junitxml=test-reports/results.xml tests/ -v
