#!/bin/bash

# Exit on any error
set -e

# Activate virtual environment
cd "$(dirname "$0")"
source .venv/bin/activate

# Start JACK if not already running

# Start a2jmidid if not running
if ! pgrep -x a2jmidid > /dev/null; then
    echo "Starting a2jmidid..."
    a2jmidid -e &
    sleep 2
fi

# Start main.py
echo "Starting FX pedal controller..."
python main.py
