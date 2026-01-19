#!/bin/bash

# Aadhaar Pulse - Quick Start Script
# This script sets up and launches the UIDAI dashboard

echo "=============================================="
echo "  🇮🇳 Aadhaar Pulse - UIDAI Dashboard"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "=============================================="
echo "  ✅ Setup Complete!"
echo "=============================================="
echo ""
echo "🚀 Starting Streamlit dashboard..."
echo "   Dashboard will open at: http://localhost:8501"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""
echo "=============================================="
echo ""

# Run the Streamlit app
python -m streamlit run app.py
