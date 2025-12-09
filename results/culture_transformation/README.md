# Culture Transformation Dashboard & Visualization

Results dashboard and visualization tools for the Culture Transformation Coach experiment.

## Available Tools

### 1. Interactive Dashboard (Streamlit)

**File**: `culture_transformation_dashboard.py`

Launch an interactive web dashboard to explore culture transformation results in real-time.

```bash
# From project root
streamlit run results/dashboards/culture_transformation_dashboard.py
```

**Features**:
- 📊 Culture health overview with key metrics
- 📈 Dimension scores radar chart
- 🏢 Sentiment distribution by department
- 📉 Trend analysis over time
- 🎯 Transformation plan visualization
- ⚠️ Risk factors identification
- 💡 Recommendations display
- 🎓 Coaching guidance viewer
- 💾 Export functionality

**Data Sources**:
- Upload custom JSON files
- Use generated sample data
- Load from saved results

### 2. Report Generator

**File**: `generate_culture_report.py`

Generate comprehensive HTML reports and static visualizations.

```python
from results.dashboards.generate_culture_report import CultureVisualizationGenerator

viz_gen = CultureVisualizationGenerator()

# Generate full HTML report
report_path = viz_gen.generate_comprehensive_report(
    survey_data=survey_responses,
    assessment=health_assessment,
    plan=transformation_plan
)

# Generate individual visualizations
gauge_fig = viz_gen.generate_health_score_gauge(score=72.5)
radar_fig = viz_gen.generate_radar_chart(dimension_scores)
heatmap_fig = viz_gen.generate_dimension_heatmap(survey_data)
```

**Available Visualizations**:
- Health score gauge chart
- Dimension radar chart
- Department heatmap
- Trend line charts
- Score distribution plots
- Comprehensive HTML reports

## Quick Start

### Option 1: Interactive Dashboard

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install streamlit plotly pandas

# Launch dashboard
streamlit run results/dashboards/culture_transformation_dashboard.py
```

### Option 2: Generate Static Report

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install matplotlib seaborn plotly pandas numpy

# Run report generator
cd results/dashboards
python generate_culture_report.py
```

## Data Format

### Survey Responses
```json
[
  {
    "response_id": "R0001",
    "timestamp": "2025-12-10T10:30:00",
    "department": "Engineering",
    "tenure_years": 3.5,
    "role_level": "Individual Contributor",
    "ratings": {
      "collaboration": {"score": 8.2, "question": "How well do teams collaborate?"},
      "innovation": {"score": 7.5, "question": "Does the org encourage innovation?"}
    },
    "open_ended": "Great team culture and supportive leadership."
  }
]
```

### Health Assessment
```json
{
  "overall_health_score": 72.5,
  "metrics": {
    "employee_engagement": 7.2,
    "retention_rate": 0.85,
    "innovation_index": 6.5
  },
  "risk_factors": [
    "Leadership communication gaps"
  ],
  "recommended_interventions": [
    "Implement quarterly town halls"
  ]
}
```

### Transformation Plan
```json
{
  "phases": {
    "short_term": ["Town halls", "Skip-level meetings"],
    "medium_term": ["Leadership training"],
    "long_term": ["Innovation labs"]
  },
  "metrics": ["Engagement score", "Innovation index"],
  "timeline": "12 months"
}
```

## Visualization Examples

### 1. Culture Health Gauge
A gauge chart showing overall culture health score (0-100) with color-coded zones:
- 0-60: Poor (Red)
- 60-70: Fair (Yellow)
- 70-80: Good (Light Green)
- 80-100: Excellent (Green)

### 2. Dimension Radar Chart
Spider/radar chart displaying scores across all 8 culture dimensions:
- Collaboration
- Innovation
- Accountability
- Transparency
- Work-Life Balance
- Leadership
- Diversity & Inclusion
- Learning & Development

### 3. Department Heatmap
Heatmap showing dimension scores broken down by department, helping identify departmental variations.

### 4. Trend Analysis
Line charts tracking key metrics over time to identify improvement or decline trends.

## Output Locations

All generated reports and visualizations are saved to:
```
results/culture_transformation/
├── culture_report_20251210_143022.html
├── dimension_heatmap.png
├── trend_analysis.png
└── dashboard_export_20251210_143022.json
```

## Dashboard Screenshots

### Main View
- Health score overview with 4 key metrics
- Interactive radar chart for dimensions
- Department comparison bar chart

### Transformation Plan View
- Phased initiatives (short/medium/long-term)
- Success metrics
- Timeline visualization

### Risk & Recommendations View
- Identified risk factors
- Prioritized recommendations
- Implementation guidance

## Integration with Experiment

The dashboard can be integrated with the Culture Transformation Coach:

```python
from experiments.culture_transformation_coach.culture_coach import CultureTransformationCoach
from results.dashboards.generate_culture_report import CultureVisualizationGenerator

# Run analysis
coach = CultureTransformationCoach()
analysis = coach.analyze_culture_survey(responses, context)
assessment = coach.assess_culture_health(metrics, historical_data)
plan = coach.generate_transformation_plan(analysis, goals)

# Generate visualizations
viz_gen = CultureVisualizationGenerator()
report_path = viz_gen.generate_comprehensive_report(responses, assessment, plan)
print(f"Report available at: {report_path}")
```

## Dependencies

```bash
# For interactive dashboard
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0

# For report generator
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
```

## Tips

1. **Dashboard Performance**: For large datasets (>1000 responses), use sampling or aggregation
2. **Export**: Use the export button to save dashboard state for later analysis
3. **Customization**: Modify color schemes and layouts in the respective Python files
4. **Automation**: Schedule report generation using cron jobs or task schedulers

## Troubleshooting

**Dashboard won't load**:
```bash
pip install --upgrade streamlit plotly
```

**Import errors**:
```bash
# Ensure you're in the project root and virtual environment is activated
cd /path/to/hr-ai-lab
source .venv/bin/activate
```

**No data showing**:
- Check that JSON files are properly formatted
- Verify file paths are correct
- Use sample data option to test dashboard functionality

## Future Enhancements

- Real-time data streaming
- Comparative analysis across time periods
- Benchmark comparisons with industry standards
- Export to PowerPoint/PDF
- Email report distribution
- API integration for HRIS data

## License

Part of HR AI Lab experiments.
