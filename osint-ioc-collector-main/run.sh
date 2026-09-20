#!/bin/bash
# IOC Collector Runner Script

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "Virtual environment created and dependencies installed."
else
    source venv/bin/activate
fi

if [ ! -f "data/ioc.db" ]; then
    echo "Database not initialized. Initializing..."
    python3 main.py --init
fi

if [ "$1" == "--schedule" ]; then
    echo "Starting scheduler daemon..."
    echo "Press Ctrl+C to stop."
    python3 main.py --schedule
elif [ "$1" == "--collect" ]; then
    echo "Running manual collection..."
    python3 main.py --collect
elif [ "$1" == "--export" ]; then
    echo "Exporting data..."
    python3 main.py --export
elif [ "$1" == "--stats" ]; then
    python3 main.py --stats
else
    python3 main.py "$@"
fi
