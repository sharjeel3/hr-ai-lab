# CV Screening Results Dashboards

This directory contains visualization and reporting tools for CV screening results.

## Available Dashboards

### 1. Interactive Dashboard (Streamlit)
**File:** `cv_screening_dashboard.py`

An interactive, real-time dashboard with:
- Overview metrics and KPIs
- Score distribution charts
- Recommendation breakdown (pie chart)
- Experience vs Score analysis
- Skills frequency analysis
- Detailed candidate profiles
- Filtering and sorting capabilities
- CSV export functionality

**Run:**
```bash
streamlit run results/dashboards/cv_screening_dashboard.py
```

**Features:**
- 📊 Multiple visualization tabs
- 🔍 Advanced filtering
- 📥 Export to CSV
- 🎯 Individual candidate analysis
- 📈 Real-time data updates

### 2. Static HTML Report
**File:** `generate_report.py`

Generates a comprehensive, printable HTML report with:
- Executive summary with key metrics
- Ranked candidate list
- Detailed candidate profiles
- Strengths, gaps, and reasoning for each candidate
- Professional styling for presentations

**Run:**
```bash
python3 results/dashboards/generate_report.py
```

**Output:**
- Self-contained HTML file
- No dependencies required to view
- Optimized for printing
- Shareable with stakeholders

## Requirements

All requirements are already in `requirements.txt`:
- `streamlit>=1.28.0` - For interactive dashboard
- `plotly>=5.17.0` - For interactive charts
- `pandas>=2.0.0` - For data manipulation

## Usage Examples

### View Latest Results
```bash
# From project root directory
cd /Users/sharjeel/dev/hr-ai-lab

# Activate virtual environment
source .venv/bin/activate

# Launch interactive dashboard
streamlit run results/dashboards/cv_screening_dashboard.py
# Opens at http://localhost:8501

# Generate static report
python3 results/dashboards/generate_report.py
# Saves to results/dashboards/cv_screening_report_[timestamp].html
```

### Run Complete Pipeline
```bash
# Make script executable (first time only)
chmod +x run_screening_with_reports.sh

# Run full pipeline: screening → report → dashboard
./run_screening_with_reports.sh
```

### Compare Different Runs
1. Run CV screening multiple times with different settings
2. Each run creates a timestamped JSON file in `results/cv_screening/`
3. Dashboard dropdown automatically lists all available results
4. Select different runs to compare metrics and rankings

### Export and Share
1. **Interactive Dashboard:**
   - Open dashboard at http://localhost:8501
   - Navigate to "Detailed Analysis" tab
   - Apply filters (score, recommendation, etc.)
   - Click "Download filtered data as CSV" button
   - Open CSV in Excel, Google Sheets, or Python

2. **Static HTML Report:**
   - Run `python3 results/dashboards/generate_report.py`
   - Open generated HTML in browser
   - Print to PDF (Ctrl/Cmd+P → Save as PDF)
   - Email or share the self-contained HTML file
   - No dependencies needed to view

## Dashboard Features

### Interactive Dashboard

**Access:** http://localhost:8501 (after running `streamlit run`)

**Navigation:**
- Use sidebar tabs to switch views
- Hover over charts for tooltips and details
- Click dropdown menus to drill into specific candidates
- Use keyboard shortcuts: `R` to rerun/refresh, `C` to clear cache

#### Overview Tab
📊 High-level metrics and visualizations:
- **Key Metrics Cards:**
  - Total candidates processed
  - Average score across all candidates
  - Recommended for hire count
  - Average years of experience
- **Score Distribution:** Interactive histogram showing score ranges
- **Recommendation Breakdown:** Pie chart of Strong Hire / Consider / Reject
- **Score vs Experience:** Scatter plot correlating experience with scores

**Use Case:** Quick assessment of screening batch quality

#### Detailed Analysis Tab
📋 Comprehensive candidate data table:
- **Sortable Columns:** Click any column header to sort (name, score, recommendation)
- **Multi-Filter System:**
  - Recommendation filter (Strong Hire, Consider, Reject, or All)
  - Minimum overall score slider (0-100)
  - Filters work together (AND logic)
- **Data Display:**
  - Candidate name and ID
  - All scores (overall, role fit, technical, experience)
  - Years of experience and education level
  - Final recommendation
- **Export:** Download filtered data as CSV for further analysis

**Use Case:** Deep-dive into specific candidate segments, export for reporting

#### Skills Analysis Tab
🎯 Aggregate skill and qualification insights:
- **Top Skills Chart:** Bar chart of most frequently required skills across all candidates
- **Education Distribution:** Pie chart showing Bachelor's, Master's, PhD breakdown
- **Experience Distribution:** Histogram of years of experience ranges
- **Skill Insights:** Identifies in-demand skills and qualification patterns

**Use Case:** Understand talent pool composition, identify skill gaps, plan training needs

#### Candidate Details Tab
👤 Individual candidate profiles:
- **Candidate Selector:** Dropdown to choose any candidate from results
- **Score Card:** Visual display of all scoring dimensions
- **Strengths Section:** ✅ Green checkmarks for key advantages
- **Gaps Section:** ❌ Red marks for areas of concern
- **AI Reasoning:** Detailed explanation of recommendation decision
- **Full Context:** Education, experience, skills, and qualifications

**Use Case:** Prepare for interviews, share with hiring managers, make final decisions

### Static HTML Report

#### Features
- Beautiful gradient metric cards
- Ranked candidate cards
- Color-coded recommendations:
  - 🟢 Strong Match
  - 🔵 Good Match
  - 🟡 Possible Match
  - 🔴 Weak Match
- Print-optimized layout
- Responsive design
- No external dependencies

## Customization

### Modify Dashboard
Edit `cv_screening_dashboard.py` to:
- Add new visualizations
- Change color schemes
- Add custom filters
- Modify metric calculations

### Modify Report
Edit `generate_report.py` to:
- Adjust HTML/CSS styling
- Add new sections
- Change ranking logic
- Include additional data

## Tips & Best Practices

### Dashboard Usage
1. **Performance:** Dashboard caches data - use `R` key to refresh if results change
2. **Filtering:** Combine filters in Detailed Analysis tab for precise candidate segments
3. **Comparison:** Open multiple browser tabs to compare different screening runs
4. **Mobile:** Dashboard is responsive - view on tablet during interviews
5. **Presentation Mode:** Use browser full-screen (F11) for stakeholder presentations

### Report Generation
1. **Timing:** Generate reports immediately after screening for archival
2. **Sharing:** HTML reports have no dependencies - safe to email
3. **Printing:** Reports are optimized for printing - use browser print dialog
4. **Branding:** Edit CSS in `generate_report.py` to add company colors/logo
5. **Archival:** Keep timestamped reports for audit trails and compliance

### Analysis Workflows
1. **Quick Review:** Use Overview tab → identify top candidates → check Details tab
2. **Deep Analysis:** Use Detailed Analysis tab → apply filters → export CSV → analyze in Excel/Python
3. **Skill Planning:** Use Skills Analysis tab → identify common gaps → plan training programs
4. **Stakeholder Sharing:** Generate HTML report → print to PDF → share via email
5. **Historical Trends:** Compare multiple screening runs → track quality improvements

## Troubleshooting

### Dashboard Issues

**Problem:** Dashboard won't start
```bash
# Solution 1: Check Streamlit installation
pip install --upgrade streamlit plotly pandas

# Solution 2: Verify you're in project root
cd /Users/sharjeel/dev/hr-ai-lab
pwd  # Should show /Users/sharjeel/dev/hr-ai-lab

# Solution 3: Activate virtual environment
source .venv/bin/activate
streamlit run results/dashboards/cv_screening_dashboard.py
```

**Problem:** Port 8501 already in use
```bash
# Solution 1: Use different port
streamlit run results/dashboards/cv_screening_dashboard.py --server.port 8502

# Solution 2: Kill existing Streamlit process
lsof -i :8501  # Find process ID
kill -9 <PID>  # Replace <PID> with actual process ID
```

**Problem:** "No results found" error
```bash
# Solution: Run CV screening first to generate results
source .venv/bin/activate
python3 experiments/recruitment_cv_screening/cv_screener.py

# Verify results exist
ls -la results/cv_screening/
# Should show screening_results_*.json files
```

**Problem:** Charts not displaying
- Clear browser cache (Ctrl+Shift+Delete)
- Ensure Plotly is installed: `pip install plotly`
- Try different browser (Chrome, Firefox, Safari)
- Check browser console (F12) for JavaScript errors

**Problem:** Dashboard shows old data
- Press `R` key in dashboard to refresh
- Or use menu: ⋮ → "Rerun"
- Or click "Clear Cache" in Streamlit menu

### Report Generation Issues

**Problem:** HTML report is blank or incomplete
```bash
# Solution 1: Verify JSON results exist and are valid
cat results/cv_screening/screening_results_*.json | python3 -m json.tool

# Solution 2: Check for error messages
python3 results/dashboards/generate_report.py 2>&1 | tee report_errors.log

# Solution 3: Ensure proper file permissions
chmod 755 results/dashboards/
```

**Problem:** Report styling looks broken
- Ensure you're opening HTML file in a modern browser (not IE)
- CSS is embedded in HTML - no external dependencies needed
- Try different browser if issues persist

**Problem:** Can't find generated report
```bash
# Reports are saved with timestamps
ls -lt results/dashboards/cv_screening_report_*.html

# Open most recent report
open results/dashboards/$(ls -t results/dashboards/cv_screening_report_*.html | head -1)
```

### General Issues

**Problem:** Google API key errors
```bash
# Verify API key is set
cat .env | grep GOOGLE_API_KEY

# Ensure .env is loaded
grep "load_dotenv" experiments/recruitment_cv_screening/cv_screener.py
```

**Problem:** Rate limiting errors
- Google free tier: 15 RPM, 250K TPM, 1000 RPD
- Wait 1-2 minutes between large screening runs
- Check rate limiter logs for details

**Problem:** Dependencies missing
```bash
# Reinstall all dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Verify specific packages
pip list | grep -E "streamlit|plotly|pandas|google-generativeai"
```

## Examples

### Quick Start
```bash
# 1. Run screening
python3 experiments/recruitment_cv_screening/cv_screener.py

# 2. View results
streamlit run results/dashboards/cv_screening_dashboard.py

# 3. Generate report
python3 results/dashboards/generate_report.py
```

### Automated Reporting
```bash
# Create a script to run screening and generate reports
./run_screening_with_reports.sh
```

## Screenshots

### Interactive Dashboard
- Multi-tab interface with charts and tables
- Real-time filtering and sorting
- Export capabilities

### HTML Report
- Executive summary at top
- Ranked candidate cards
- Detailed profiles with strengths/gaps
- Print-friendly format

## Advanced Customization

### Modify Dashboard Appearance

Edit `cv_screening_dashboard.py`:
```python
# Change theme colors (around line 10)
st.set_page_config(
    page_title="CV Screening Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modify chart colors
color_scheme = px.colors.qualitative.Set3  # Try: Plotly, D3, G10
```

### Add Custom Metrics

1. Modify CV screener to output new fields in JSON
2. Update dashboard to read and display new metrics:
```python
# In cv_screening_dashboard.py, add new column:
df['custom_metric'] = df['results'].apply(lambda x: x.get('custom_field'))
```

### Change Report Styling

Edit `generate_report.py` CSS section (around line 50):
```css
/* Change primary color */
.metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }

/* Adjust fonts */
body { font-family: 'Helvetica Neue', Arial, sans-serif; }

/* Modify card spacing */
.candidate-card { margin: 20px 0; padding: 25px; }
```

### Filter by Custom Criteria

Add filters to dashboard:
```python
# In Detailed Analysis tab
min_experience = st.slider("Minimum Years of Experience", 0, 20, 0)
filtered_df = df[df['years_of_experience'] >= min_experience]
```

## Data Schema

Expected JSON structure:
```json
{
  "experiment_id": "cv_screening_20251204_232953",
  "timestamp": "2024-12-04T23:29:53",
  "config": {
    "llm_model": "gemini-2.5-flash-lite",
    "llm_provider": "google"
  },
  "results": [
    {
      "cv_id": "cv_001_senior_engineer",
      "candidate_name": "John Doe",
      "overall_score": 85,
      "role_fit_score": 90,
      "technical_skills_score": 88,
      "experience_alignment": 82,
      "recommendation": "Strong Hire",
      "strengths": ["10+ years experience", "Leadership skills"],
      "gaps": ["No cloud certifications"],
      "reasoning": "Strong technical background...",
      "years_of_experience": 8,
      "education_level": "Master's Degree"
    }
  ]
}
```

## Performance Optimization

### For Large Datasets (100+ candidates)

1. **Enable caching:**
```python
@st.cache_data
def load_results():
    # Your loading logic
```

2. **Use pagination:**
```python
page_size = 20
page = st.number_input("Page", 1, len(df) // page_size + 1)
start = (page - 1) * page_size
end = start + page_size
st.dataframe(df.iloc[start:end])
```

3. **Optimize chart rendering:**
- Limit data points in scatter plots
- Use `st.plotly_chart(..., use_container_width=True)` → deprecated, use `width='stretch'`
- Consider aggregating data for large datasets

## Integration Examples

### Export to Google Sheets
```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# After filtering in dashboard
filtered_df.to_csv('temp.csv', index=False)
# Upload temp.csv to Google Sheets via API
```

### Email Report Automatically
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# After generating HTML report
with open('report.html', 'r') as f:
    html_content = f.read()

msg = MIMEMultipart('alternative')
msg['Subject'] = 'CV Screening Results'
msg.attach(MIMEText(html_content, 'html'))
# Send via SMTP
```

### Webhook Integration
```bash
# Notify Slack after screening completes
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  -H 'Content-Type: application/json' \
  -d '{"text":"CV screening complete! View results at http://localhost:8501"}'
```

## Support & Resources

**Documentation:**
- Main project: `README.MD`
- Setup guide: `docs/SETUP.md`
- Gemini migration: `docs/gemini-migration-guide.md`

**External Resources:**
- Streamlit docs: https://docs.streamlit.io/
- Plotly docs: https://plotly.com/python/
- Pandas docs: https://pandas.pydata.org/docs/

**Troubleshooting Checklist:**
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] Results exist in `results/cv_screening/`
- [ ] GOOGLE_API_KEY set in `.env`
- [ ] Running from project root directory
- [ ] Port 8501 not in use
- [ ] Browser is modern (Chrome, Firefox, Safari)

**Getting Help:**
1. Check troubleshooting section above
2. Review error messages carefully
3. Verify JSON file structure
4. Check file permissions
5. Try with a fresh virtual environment

## Future Enhancements

Planned features:
- [ ] Multi-experiment comparison dashboard
- [ ] Historical trend analysis across screening runs
- [ ] Advanced search/filter by skills, education, location
- [ ] Direct PDF export from dashboard
- [ ] Email automation for report distribution
- [ ] ATS integration (Greenhouse, Lever, Workday)
- [ ] Candidate ranking algorithms
- [ ] Bias detection and fairness metrics
- [ ] Interview scheduling integration
- [ ] Mobile app version
