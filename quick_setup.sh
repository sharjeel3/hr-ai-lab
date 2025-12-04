#!/bin/bash
# Quick setup helper for Google Gemini API

echo "🚀 HR AI Lab - Google Gemini Quick Setup"
echo "=========================================="
echo ""

# Step 1: Install Google Generative AI package
echo "📦 Step 1: Installing google-generativeai package..."
pip3 install google-generativeai

if [ $? -eq 0 ]; then
    echo "✅ Package installed successfully"
else
    echo "❌ Failed to install package"
    exit 1
fi

echo ""

# Step 2: Check for .env file
if [ ! -f ".env" ]; then
    echo "📝 Step 2: Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

echo ""

# Step 3: Check for API key
if grep -q "GOOGLE_API_KEY=your_google_api_key_here" .env 2>/dev/null || ! grep -q "GOOGLE_API_KEY=" .env 2>/dev/null; then
    echo "⚠️  Step 3: Configure your Google API key"
    echo ""
    echo "You need to:"
    echo "1. Visit: https://aistudio.google.com/app/apikey"
    echo "2. Sign in and create an API key"
    echo "3. Add it to the .env file:"
    echo ""
    echo "   Open .env file and replace:"
    echo "   GOOGLE_API_KEY=your_google_api_key_here"
    echo "   with:"
    echo "   GOOGLE_API_KEY=your_actual_key"
    echo ""
    read -p "Press Enter when you've added your API key..."
else
    echo "✅ GOOGLE_API_KEY appears to be configured"
fi

echo ""
echo "🧪 Step 4: Running integration tests..."
python3 scripts/test_gemini_integration.py

echo ""
echo "=========================================="
echo "Setup complete! 🎉"
echo ""
echo "Next steps:"
echo "1. If tests passed, run an experiment:"
echo "   python3 experiments/recruitment_cv_screening/cv_screener.py"
echo ""
echo "2. Check the documentation:"
echo "   docs/gemini-migration-guide.md"
echo "   docs/SETUP.md"
echo ""
