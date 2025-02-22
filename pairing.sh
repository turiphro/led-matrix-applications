#!/bin/bash

# Check if .venv directory exists
if [ ! -d ".venv" ]; then
    ./install.sh
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Run the Python script
echo "Running pair_controllers.py..."
cd src
python pair_controllers.py

