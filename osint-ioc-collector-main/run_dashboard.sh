#!/bin/bash
# IOC Collector Dashboard Launcher

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
    echo "⚠️  Warning: Database not initialized."
    echo "Run './run.sh --init' first to initialize the database."
    echo ""
    read -p "Do you want to initialize now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 main.py --init
    else
        exit 1
    fi
fi

echo ""
echo "======================================"
echo "  IOC Collector Dashboard"
echo "======================================"
echo ""
echo "🚀 Starting dashboard..."
echo "📊 Dashboard will be available at:"
echo "   http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 -m web.app
