# Interview Summarization Dashboard

Interactive visualization dashboard for AI-powered interview analysis results.

## Features

### 📊 Visualizations

1. **Metrics Summary** - Key performance indicators at a glance
   - Total interviews processed
   - Average candidate score
   - Hiring recommendation distribution

2. **Candidate Scores** - Bar chart showing overall scores by candidate
   - Color-coded by recommendation (Strong Hire, Hire, Maybe, No Hire)

3. **Recommendation Distribution** - Pie chart of hiring recommendations
   - Visual breakdown of hiring decisions

4. **Confidence Levels** - Scatter plot showing assessment confidence
   - Bubble size represents candidate score

5. **Interview Duration** - Bar chart of interview lengths
   - Helps identify patterns in interview timing

6. **Competency Comparison** - Radar chart comparing candidates
   - Technical vs behavioral competencies

7. **Candidate Cards** - Detailed cards for each candidate
   - Score, recommendation, and key highlights

## Usage

### Generate Dashboard from Latest Results

```bash
python3 results/dashboards/interview_summarization_dashboard.py \
  --summaries results/interview_summarization/interview_summaries_TIMESTAMP.json \
  --metrics results/interview_summarization/summarization_metrics_TIMESTAMP.json \
  --rankings results/interview_summarization/candidate_rankings_TIMESTAMP.json
```

### Auto-generation

The dashboard is automatically generated when running the interview summarizer:

```bash
python3 experiments/interview_summarisation/interview_summarizer.py
```

The dashboard HTML file will be saved to `results/dashboards/interview_dashboard_TIMESTAMP.html`

## Viewing the Dashboard

Simply open the generated HTML file in any web browser:

```bash
open results/dashboards/interview_dashboard_TIMESTAMP.html
```

Or drag and drop the HTML file into your browser.

## Dashboard Components

### Color Coding

- 🟢 **Strong Hire** - Green (Score typically 85+)
- 🔵 **Hire** - Blue (Score typically 75-84)
- 🟡 **Maybe** - Amber (Score typically 60-74)
- 🔴 **No Hire** - Red (Score below 60)

### Metrics Explained

- **Overall Score**: Composite score out of 100 based on technical and behavioral assessment
- **Confidence Level**: AI's confidence in the assessment (High/Medium/Low)
- **Interview Duration**: Length of interview in minutes
- **Recommendation**: Final hiring recommendation

## Requirements

- Python 3.8+
- plotly >= 5.17.0
- pandas >= 2.0.0

## Output Format

The dashboard is a standalone HTML file with embedded JavaScript for interactivity. No server required - works offline!

## Customization

You can customize the dashboard by editing `interview_summarization_dashboard.py`:

- Adjust color schemes in the color_map dictionaries
- Modify chart layouts and sizes
- Add additional visualizations
- Change scoring thresholds

## Troubleshooting

**Missing dependencies:**
```bash
pip install plotly pandas
```

**Dashboard not generating:**
- Check that all JSON files exist
- Verify file paths are correct
- Ensure results contain valid data

## Examples

See `results/dashboards/` for example dashboards generated from interview results.
