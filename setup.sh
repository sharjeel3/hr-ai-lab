#!/bin/bash
# Setup script for HR AI Lab

echo "🚀 Setting up HR AI Lab..."

# Check if .venv exists
if [ -d ".venv" ]; then
    echo "✅ Virtual environment already exists"
else
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ -f ".env" ]; then
    echo "✅ .env file already exists"
else
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run an experiment:"
echo "  python scripts/run_experiment.py --experiment cv_screening"
echo ""
