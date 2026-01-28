#!/bin/bash
# ISODROP - Real-time Local Wi-Fi Data Sharing
# Quick Start Script for macOS/Linux

echo ""
echo "========================================"
echo "   ISODROP - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

echo "[OK] Python3 found"
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] pip3 is not available"
    exit 1
fi

echo "[OK] pip3 found"
echo ""

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install requirements
echo "[*] Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo "[OK] Dependencies installed"
echo ""

# Start the server
echo "[*] Starting ISODROP server..."
echo ""
python3 app.py
