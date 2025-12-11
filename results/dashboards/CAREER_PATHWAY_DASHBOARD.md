# Career Pathway Dashboard Quick Start

## 🚀 Launch Options

### Option 1: Interactive Streamlit Dashboard (Recommended)

```bash
cd results/dashboards
streamlit run career_pathway_dashboard.py
```

**Features:**
- Real-time filtering and exploration
- Interactive charts (zoom, pan, hover)
- Employee-by-employee drill-down
- Career pathway network visualization
- Skill gap analysis

**Requirements:**
```bash
pip install streamlit plotly pandas numpy
```

### Option 2: Static HTML Report

```bash
cd results/dashboards
python generate_career_pathway_report.py
```

**Features:**
- Self-contained HTML file
- No server required
- Shareable via email/drive
- All visualizations embedded
- Professional formatting

### Option 3: Dashboard Launcher (All-in-One)

```bash
cd results/dashboards
python launch_dashboard.py
```

Then select option 6 (Career Pathway Dashboard) or option 7 (HTML Report).

---

## 📊 Dashboard Features

### Overview Tab
- **Metrics Cards**: Total employees, success rate, average match score, unique roles
- **Score Distribution**: Histogram of match scores with mean line
- **Job Family Breakdown**: Pie chart of recommendations by department
- **Top Roles**: Bar chart of most recommended positions
- **Experience Levels**: Distribution of recommended role experience requirements

### Employee Details Tab
- **Employee Selector**: Browse all analyzed employees
- **Recommendation Cards**: Detailed breakdown of each career path
  - Match score with color coding (excellent/good/fair)
  - Role details (title, family, level, salary)
  - Key responsibilities
  - Required skills (with badges)
  - Personalized explanation
  - 90-day development plan with monthly objectives

### Analytics Tab
- **Most In-Demand Skills**: Bar chart showing skill frequency
- **Summary Statistics**: Mean, median, standard deviation of scores
- **Skill Gap Analysis**: Identify common skills across recommendations

### Career Pathways Tab
- **Network Visualization**: Interactive graph showing career transitions
- **Current Role → Recommended Role**: Visual mapping of pathways
- **Edge Thickness**: Represents frequency of specific transitions

---

## 🎨 Dashboard Screenshots

### Overview
- Clean, modern interface with gradient header
- Metric cards with real-time data
- Interactive Plotly charts

### Employee Cards
- Color-coded match scores:
  - 🟢 Green (80%+): Excellent match
  - 🔵 Blue (70-80%): Good match
  - 🟡 Yellow (<70%): Fair match
- Skill badges in brand colors
- Expandable development plans

### Filters
- Minimum match score slider
- Real-time result filtering
- Preserves all visualizations

---

## 📁 File Structure

```
results/dashboards/
├── career_pathway_dashboard.py          # Streamlit interactive dashboard
├── generate_career_pathway_report.py    # HTML report generator
├── launch_dashboard.py                   # Unified launcher (updated)
├── career_pathway_report_TIMESTAMP.html # Generated reports
└── CAREER_PATHWAY_DASHBOARD.md          # This file
```

---

## 🔧 Customization

### Change Color Scheme

Edit `career_pathway_dashboard.py`:

```python
# Line ~33-37: Update CSS colors
.metric-card {
    background-color: #YOUR_COLOR;
    border-left: 4px solid #YOUR_ACCENT;
}
```

### Add Custom Visualizations

```python
def create_custom_chart(recommendations):
    # Your visualization logic
    fig = go.Figure(...)
    return fig

# Add to tab4 section
st.plotly_chart(create_custom_chart(recommendations))
```

### Export Data

Add data export buttons:

```python
# In dashboard
if st.button("Export to CSV"):
    df.to_csv('career_recommendations.csv', index=False)
    st.success("Exported!")
```

---

## 🐛 Troubleshooting

### "No recommendation results found"

**Solution:** Run the experiment first:
```bash
cd experiments/career_pathway_recommender
python run_career_pathway.py
```

### "Streamlit not found"

**Solution:** Install dependencies:
```bash
pip install streamlit plotly pandas numpy
```

### Port already in use

**Solution:** Specify different port:
```bash
streamlit run career_pathway_dashboard.py --server.port 8502
```

### Charts not rendering in HTML report

**Solution:** Ensure internet connection (Plotly CDN required) or use:
```python
fig.to_html(include_plotlyjs='inline')  # Embeds Plotly.js
```

---

## 📊 Data Sources

The dashboard reads from:
```
results/career_pathway/
├── recommendations_TIMESTAMP.json  # Main recommendation data
├── metrics_TIMESTAMP.json          # Aggregated metrics
└── report_TIMESTAMP.txt            # Text-based report
```

Data structure:
```json
{
  "recommendations": [
    {
      "employee_id": "EMP001",
      "employee_name": "...",
      "current_title": "...",
      "recommendations": [
        {
          "role": { ... },
          "similarity_score": 0.87,
          "explanation": "...",
          "development_plan": { ... }
        }
      ]
    }
  ],
  "metrics": {
    "total_employees": 4,
    "success_rate": 1.0,
    "average_similarity_score": 0.82,
    "unique_roles_recommended": 8
  }
}
```

---

## 🚀 Advanced Usage

### Batch Analysis

Compare multiple experiment runs:

```python
# Load multiple results
results_list = []
for file in Path('results/career_pathway').glob('recommendations_*.json'):
    results_list.append(load_json_data(file))

# Aggregate metrics
avg_scores = [r['metrics']['average_similarity_score'] for r in results_list]
```

### Integration with BI Tools

Export to formats for Tableau/PowerBI:

```python
# Convert to flat DataFrame
import pandas as pd

rows = []
for rec in recommendations:
    for item in rec['recommendations']:
        rows.append({
            'employee_id': rec['employee_id'],
            'employee_name': rec['employee_name'],
            'current_title': rec['current_title'],
            'recommended_role': item['role']['title'],
            'job_family': item['role']['job_family'],
            'match_score': item['similarity_score'],
            'salary_range': item['role']['salary_range']
        })

df = pd.DataFrame(rows)
df.to_csv('career_pathways_flat.csv', index=False)
```

### Scheduled Reports

Create cron job for automated reports:

```bash
# Add to crontab
0 9 * * 1 cd /path/to/hr-ai-lab/results/dashboards && python generate_career_pathway_report.py --output weekly_report.html
```

---

## 📚 Related Documentation

- [Career Pathway Recommender README](../../experiments/career_pathway_recommender/README.md)
- [Implementation Plan](../../docs/implementation-plan.md)
- [Main Repository README](../../README.MD)

---

## 🤝 Contributing

To add new visualizations or features:

1. Add chart function to `career_pathway_dashboard.py`
2. Call from appropriate tab
3. Update this documentation
4. Test with sample data

---

## 📝 License

See main repository LICENSE file.

---

**Last Updated**: December 2025  
**Status**: ✅ Complete - Dashboards & Visualizations Implemented
