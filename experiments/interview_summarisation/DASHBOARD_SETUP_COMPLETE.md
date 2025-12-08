# Interview Summarization Dashboard - Setup Complete! 🎉

## What Was Created

### 1. Dashboard Generator (`results/dashboards/interview_summarization_dashboard.py`)
A comprehensive Python script that generates interactive HTML dashboards with:
- 📊 Candidate score visualizations
- 🥧 Recommendation distribution charts
- 🎯 Confidence level indicators
- ⏱️ Interview duration analysis
- 🕸️ Competency comparison radar charts
- 🃏 Detailed candidate cards with highlights

### 2. Convenience Scripts

**Bash Script** (`experiments/interview_summarisation/generate_dashboard.sh`)
- Automatically finds latest results
- Generates dashboard
- Offers to open in browser

**Python Viewer** (`experiments/interview_summarisation/view_dashboard.py`)
- Quickly opens the most recent dashboard
- Simple one-command access

### 3. Auto-Generation Integration
The interview summarizer now automatically generates dashboards after processing interviews!

### 4. Documentation
- `DASHBOARD_README.md` - Complete dashboard documentation
- Updated main `README.md` with dashboard features

## How to Use

### Option 1: Auto-generate with Interview Summarizer
```bash
python3 experiments/interview_summarisation/interview_summarizer.py
```
Dashboard is automatically created at: `results/dashboards/interview_dashboard_TIMESTAMP.html`

### Option 2: Generate from Existing Results
```bash
./experiments/interview_summarisation/generate_dashboard.sh
```

### Option 3: View Latest Dashboard
```bash
python3 experiments/interview_summarisation/view_dashboard.py
```

### Option 4: Manual Generation
```bash
python3 results/dashboards/interview_summarization_dashboard.py \
  --summaries results/interview_summarization/interview_summaries_TIMESTAMP.json \
  --metrics results/interview_summarization/summarization_metrics_TIMESTAMP.json \
  --rankings results/interview_summarization/candidate_rankings_TIMESTAMP.json
```

## Dashboard Features

### Visual Components
1. **Metrics Summary Cards** - 6 KPI indicators with gauges
2. **Candidate Scores Bar Chart** - Color-coded by recommendation
3. **Recommendation Pie Chart** - Distribution of hiring decisions
4. **Confidence Scatter Plot** - Bubble chart with score-based sizing
5. **Duration Bar Chart** - Interview length analysis
6. **Competency Radar Chart** - Multi-dimensional comparison
7. **Candidate Detail Cards** - Rich cards with highlights

### Color Coding
- 🟢 Strong Hire (85+ score)
- 🔵 Hire (75-84 score)
- 🟡 Maybe (60-74 score)
- 🔴 No Hire (<60 score)

### Interactive Features
- Hover tooltips with detailed information
- Responsive layout
- Standalone HTML (works offline)
- No server required
- Beautiful gradient header

## Files Created

```
results/dashboards/
├── interview_summarization_dashboard.py    # Main generator
└── interview_dashboard_TIMESTAMP.html      # Generated dashboards

experiments/interview_summarisation/
├── DASHBOARD_README.md                     # Dashboard docs
├── generate_dashboard.sh                   # Quick generator script
├── view_dashboard.py                       # Dashboard viewer
└── README.md                               # Updated with dashboard info
```

## Current Dashboard

Your first dashboard has been generated and opened in your browser:
📂 `results/dashboards/interview_dashboard_20251208_112825.html`

## Next Steps

1. **View the dashboard** - It should be open in your browser
2. **Run more interviews** - Generate new data to see updated dashboards
3. **Customize** - Edit `interview_summarization_dashboard.py` to adjust colors, layouts, or add new charts
4. **Share** - The HTML files are standalone and can be shared via email or web hosting

## Dependencies

Already installed in your virtual environment:
- ✅ plotly >= 5.17.0
- ✅ pandas >= 2.0.0

## Troubleshooting

**Dashboard not generating?**
- Ensure results exist in `results/interview_summarization/`
- Check that JSON files are valid
- Verify plotly and pandas are installed

**Can't open dashboard?**
- Try: `open results/dashboards/interview_dashboard_TIMESTAMP.html`
- Or drag the HTML file into your browser

**Charts not displaying?**
- Check browser console for errors
- Ensure internet connection (for Plotly CDN)
- Try a different browser

## Tips

- Dashboards are timestamped - you can keep a history
- Each run of the interview summarizer creates a new dashboard
- Compare dashboards across different interview batches
- Use the generated HTML in reports or presentations

---

**Enjoy your new interview analytics dashboard! 🚀**
