# HR AI Lab - Dashboard Quick Start

## 🚀 Get Started in 30 Seconds

### Option 1: Static HTML Dashboard (Easiest)

```bash
# Generate dashboard
python results/dashboards/generate_unified_dashboard.py

# Open in browser
open results/dashboards/unified_dashboard_*.html
```

✅ **No dependencies** • Works offline • Easy to share

---

### Option 2: Interactive Streamlit App (Most Powerful)

```bash
# Install dependencies (one time)
pip install streamlit plotly pandas

# Run dashboard
streamlit run results/dashboards/unified_streamlit_dashboard.py
```

✅ **Real-time updates** • Interactive charts • Advanced filters

---

## 📊 What You'll See

### HTML Dashboard
- 🎯 Experiment completion overview (5/5 experiments)
- 📊 Data Quality Score: 45.25/100
- 🔍 29 issues detected across 19 records
- ⚖️ Bias testing status
- 📈 Interactive charts

### Streamlit Dashboard
- Multiple pages for deep analysis
- Real-time data refresh
- Interactive filters
- Comparative views
- Export capabilities

---

## 🎨 Dashboard Features

### Overview Metrics
```
✓ Experiments Run: 5/5 (100% Complete)
✓ Data Quality Score: 45.25/100  
✓ Bias Reports: Available
✓ Total Issues Found: 29
```

### Data Quality Insights
- Quality score gauge (0-100)
- Issues by type (bar chart)
- Issues by severity (pie chart)
- Recommendations list
- Auto-fix suggestions

### Visualizations
- 📊 Bar charts (issues by type)
- 🥧 Pie charts (severity distribution)
- 📈 Gauges (quality scores)
- 🎯 Progress bars (completion status)

---

## 📁 Generated Files

### HTML Dashboard
```
results/dashboards/unified_dashboard_20251211_101645.html
```
- Self-contained (all CSS/JS embedded)
- Works offline
- Easy to email/share
- Professional appearance

### Streamlit App
```
Run on: http://localhost:8501
```
- Real-time updates
- Interactive exploration
- Multiple pages
- Export options

---

## 🔄 Updating Data

Dashboards automatically load the **most recent** results from each experiment:

- `results/hris_data_quality/` - Latest quality report
- `results/bias_testing/` - Latest bias test
- `results/cv_screening/` - Latest screening results
- `results/interview_summarization/` - Latest summaries
- `results/culture_transformation/` - Latest insights

To update:
1. Run experiments to generate new results
2. Regenerate dashboard
3. Refresh browser (HTML) or click "Refresh Data" (Streamlit)

---

## 💡 Tips & Tricks

### HTML Dashboard
- **Share results**: Just send the HTML file
- **Print reports**: Use browser print function
- **Archive versions**: HTML files include timestamp
- **Mobile friendly**: Responsive design works on phones

### Streamlit Dashboard
- **Refresh data**: Click "🔄 Refresh Data" in sidebar
- **Multiple views**: Use navigation menu for different pages
- **Export data**: Charts can be downloaded as images
- **Full screen**: Use F11 for immersive view

---

## 🎯 Example Use Cases

### 1. Weekly Team Review
```bash
# Generate fresh dashboard
python results/dashboards/generate_unified_dashboard.py

# Email HTML file to team
# Everyone can view without setup
```

### 2. Live Presentation
```bash
# Start interactive dashboard
streamlit run results/dashboards/unified_streamlit_dashboard.py

# Present in browser
# Real-time interaction with data
```

### 3. Executive Summary
```bash
# HTML dashboard provides:
- High-level metrics
- Visual appeal
- Professional format
- Easy to digest
```

### 4. Deep Analysis
```bash
# Streamlit provides:
- Drill-down capabilities
- Interactive filters
- Comparative analysis
- Export options
```

---

## 📈 Current Status

```
✅ Unified HTML Dashboard - OPERATIONAL
✅ Unified Streamlit Dashboard - OPERATIONAL  
✅ Data Quality Visualizations - COMPLETE
✅ Bias Testing Views - COMPLETE
✅ CV Screening Dashboard - OPERATIONAL
✅ Interview Dashboard - OPERATIONAL
✅ Culture Dashboard - OPERATIONAL
```

---

## 🚨 Troubleshooting

### "No results found"
```bash
# Run experiments first
python experiments/hris_data_quality_agent/example_quality_check.py
python experiments/ethical_ai_bias_tests/example_bias_test.py
```

### "Module not found" (Streamlit)
```bash
# Install dependencies
pip install streamlit plotly pandas
```

### Dashboard looks broken
```bash
# Ensure you're using a modern browser
# Chrome, Firefox, Safari, Edge all supported
```

---

## 🎓 Next Steps

1. ✅ Generate HTML dashboard for static reporting
2. ✅ Run Streamlit for interactive exploration  
3. ✅ Run more experiments to populate data
4. ✅ Share HTML reports with stakeholders
5. ✅ Use Streamlit for team analysis sessions

---

**Built with ❤️ for the HR AI Lab**
