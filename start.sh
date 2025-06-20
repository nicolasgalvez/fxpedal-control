#!/bin/bash

# Exit on any error
set -e

# Activate virtual environment
cd "$(dirname "$0")"
source .venv/bin/activate

# Start JACK if not already running
if ! pgrep -x jackd > /dev/null; then
    echo "Starting JACK..."
    jackd -dalsa -dhw:3,0 -r41000 -p1024 -n2 &
    sleep 3
fi

# Start a2jmidid if not running
if ! pgrep -x a2jmidid > /dev/null; then
    echo "Starting a2jmidid..."
    a2jmidid -e &
    sleep 2
fi

# Start main.py
echo "Starting FX pedal controller..."
python main.py
