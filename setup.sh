#!/bin/bash

echo "Setting up virtual environment..."

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install -r requirements.txt
else
  echo "No requirements.txt found. Creating a fresh one..."
  pip install python-rtmidi
  pip freeze > requirements.txt
fi

echo "✅ Setup complete. Virtual environment is ready."
