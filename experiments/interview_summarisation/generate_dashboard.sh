#!/bin/bash
# Quick dashboard generator for interview summarization results

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎨 Interview Summarization Dashboard Generator${NC}"
echo ""

# Check if results directory exists
if [ ! -d "results/interview_summarization" ]; then
    echo -e "${YELLOW}⚠️  No interview summarization results found${NC}"
    echo "Run the interview summarizer first:"
    echo "  python3 experiments/interview_summarisation/interview_summarizer.py"
    exit 1
fi

# Find latest results
LATEST_SUMMARIES=$(ls -t results/interview_summarization/interview_summaries_*.json 2>/dev/null | head -1)
LATEST_METRICS=$(ls -t results/interview_summarization/summarization_metrics_*.json 2>/dev/null | head -1)
LATEST_RANKINGS=$(ls -t results/interview_summarization/candidate_rankings_*.json 2>/dev/null | head -1)

if [ -z "$LATEST_SUMMARIES" ]; then
    echo -e "${YELLOW}⚠️  No interview summary files found${NC}"
    exit 1
fi

echo -e "${GREEN}📊 Found latest results:${NC}"
echo "  Summaries: $(basename $LATEST_SUMMARIES)"
echo "  Metrics:   $(basename $LATEST_METRICS)"
echo "  Rankings:  $(basename $LATEST_RANKINGS)"
echo ""

# Generate dashboard
echo -e "${BLUE}🔨 Generating dashboard...${NC}"
python3 results/dashboards/interview_summarization_dashboard.py \
    --summaries "$LATEST_SUMMARIES" \
    --metrics "$LATEST_METRICS" \
    --rankings "$LATEST_RANKINGS"

# Find the generated dashboard
LATEST_DASHBOARD=$(ls -t results/dashboards/interview_dashboard_*.html 2>/dev/null | head -1)

if [ -n "$LATEST_DASHBOARD" ]; then
    echo ""
    echo -e "${GREEN}✅ Dashboard generated successfully!${NC}"
    echo -e "${GREEN}📂 Location: $LATEST_DASHBOARD${NC}"
    echo ""
    
    # Offer to open in browser
    read -p "Open dashboard in browser? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open "$LATEST_DASHBOARD"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            xdg-open "$LATEST_DASHBOARD"
        else
            echo "Please open manually: $LATEST_DASHBOARD"
        fi
    fi
else
    echo -e "${YELLOW}⚠️  Dashboard file not found${NC}"
    exit 1
fi
