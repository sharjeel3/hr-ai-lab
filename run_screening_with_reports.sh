#!/bin/bash
# Automated CV Screening with Dashboard Generation

echo "🚀 Running CV Screening with Automated Reporting"
echo "================================================"
echo ""

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

echo ""
echo "📊 Step 1: Running CV Screening..."
python3 experiments/recruitment_cv_screening/cv_screener.py

if [ $? -eq 0 ]; then
    echo "✅ CV Screening completed successfully"
else
    echo "❌ CV Screening failed"
    exit 1
fi

echo ""
echo "📄 Step 2: Generating HTML Report..."
python3 results/dashboards/generate_report.py

if [ $? -eq 0 ]; then
    echo "✅ HTML Report generated successfully"
else
    echo "❌ HTML Report generation failed"
    exit 1
fi

echo ""
echo "🎉 All Done!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. View interactive dashboard:"
echo "   streamlit run results/dashboards/cv_screening_dashboard.py"
echo ""
echo "2. Open HTML report:"
echo "   open results/dashboards/cv_screening_report_*.html"
echo ""
echo "3. Check results directory:"
echo "   ls -lah results/cv_screening/"
echo ""
