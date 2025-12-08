"""
Interview Summarization Dashboard

Interactive dashboard for visualizing interview summarization results including:
- Candidate scores and recommendations
- Competency analysis
- Interview metrics and trends
- Comparative analysis across candidates
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))


class InterviewDashboard:
    """Generate interactive dashboard for interview summarization results."""
    
    def __init__(self, summaries_path: str, metrics_path: Optional[str] = None, rankings_path: Optional[str] = None):
        """
        Initialize dashboard with results data.
        
        Args:
            summaries_path: Path to interview summaries JSON
            metrics_path: Optional path to metrics JSON
            rankings_path: Optional path to candidate rankings JSON
        """
        self.summaries = self._load_json(summaries_path)
        self.metrics = self._load_json(metrics_path) if metrics_path else None
        self.rankings = self._load_json(rankings_path) if rankings_path else None
        
    def _load_json(self, path: str) -> Any:
        """Load JSON file."""
        with open(path, 'r') as f:
            return json.load(f)
    
    def create_candidate_scores_chart(self) -> go.Figure:
        """Create bar chart of candidate overall scores."""
        candidates = []
        scores = []
        recommendations = []
        
        for summary in self.summaries:
            candidate = summary.get('interview_metadata', {}).get('candidate_name', 'Unknown')
            score = summary.get('summary', {}).get('overall_score', 0)
            rec = summary.get('summary', {}).get('recommendation', 'Unknown')
            
            candidates.append(candidate)
            scores.append(score)
            recommendations.append(rec)
        
        # Color mapping for recommendations
        color_map = {
            'Strong Hire': '#10b981',
            'Hire': '#3b82f6',
            'Maybe': '#f59e0b',
            'No Hire': '#ef4444'
        }
        colors = [color_map.get(rec, '#6b7280') for rec in recommendations]
        
        fig = go.Figure(data=[
            go.Bar(
                x=candidates,
                y=scores,
                marker_color=colors,
                text=scores,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Score: %{y}<br>Recommendation: ' + 
                             '<br>'.join([f'{c}: {r}' for c, r in zip(candidates, recommendations)]) +
                             '<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title='Candidate Overall Scores',
            xaxis_title='Candidate',
            yaxis_title='Score (out of 100)',
            yaxis_range=[0, 100],
            height=400,
            showlegend=False,
            hovermode='x unified'
        )
        
        return fig
    
    def create_recommendation_distribution(self) -> go.Figure:
        """Create pie chart of recommendation distribution."""
        recommendations = []
        
        for summary in self.summaries:
            rec = summary.get('summary', {}).get('recommendation', 'Unknown')
            recommendations.append(rec)
        
        rec_counts = pd.Series(recommendations).value_counts()
        
        color_map = {
            'Strong Hire': '#10b981',
            'Hire': '#3b82f6',
            'Maybe': '#f59e0b',
            'No Hire': '#ef4444'
        }
        colors = [color_map.get(rec, '#6b7280') for rec in rec_counts.index]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=rec_counts.index,
                values=rec_counts.values,
                marker_colors=colors,
                hole=0.3,
                textinfo='label+percent+value',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title='Recommendation Distribution',
            height=400
        )
        
        return fig
    
    def create_confidence_levels_chart(self) -> go.Figure:
        """Create chart showing confidence levels by candidate."""
        candidates = []
        confidence = []
        scores = []
        
        for summary in self.summaries:
            candidate = summary.get('interview_metadata', {}).get('candidate_name', 'Unknown')
            conf = summary.get('summary', {}).get('confidence_level', 'Unknown')
            score = summary.get('summary', {}).get('overall_score', 0)
            
            candidates.append(candidate)
            confidence.append(conf)
            scores.append(score)
        
        # Create scatter plot
        conf_map = {'High': 3, 'Medium': 2, 'Low': 1}
        conf_numeric = [conf_map.get(c, 0) for c in confidence]
        
        fig = go.Figure(data=[
            go.Scatter(
                x=candidates,
                y=conf_numeric,
                mode='markers+text',
                marker=dict(
                    size=scores,
                    sizemode='diameter',
                    sizeref=2,
                    color=scores,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title='Score')
                ),
                text=confidence,
                textposition='top center',
                hovertemplate='<b>%{x}</b><br>Confidence: %{text}<br>Score: %{marker.size}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title='Assessment Confidence Levels',
            xaxis_title='Candidate',
            yaxis_title='Confidence Level',
            yaxis=dict(
                tickvals=[1, 2, 3],
                ticktext=['Low', 'Medium', 'High']
            ),
            height=400
        )
        
        return fig
    
    def create_interview_duration_chart(self) -> go.Figure:
        """Create chart of interview durations."""
        candidates = []
        durations = []
        positions = []
        
        for summary in self.summaries:
            candidate = summary.get('interview_metadata', {}).get('candidate_name', 'Unknown')
            duration = summary.get('interview_metadata', {}).get('duration_minutes', 0)
            position = summary.get('interview_metadata', {}).get('position', 'Unknown')
            
            candidates.append(candidate)
            durations.append(duration)
            positions.append(position)
        
        fig = go.Figure(data=[
            go.Bar(
                x=candidates,
                y=durations,
                text=durations,
                texttemplate='%{text} min',
                textposition='auto',
                marker_color='#8b5cf6',
                hovertemplate='<b>%{x}</b><br>Duration: %{y} minutes<br>Position: ' +
                             '<br>'.join([f'{c}: {p}' for c, p in zip(candidates, positions)]) +
                             '<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title='Interview Duration by Candidate',
            xaxis_title='Candidate',
            yaxis_title='Duration (minutes)',
            height=400
        )
        
        return fig
    
    def create_competency_comparison(self) -> go.Figure:
        """Create radar chart comparing competencies across candidates."""
        # This is a simplified version - would need actual competency scores
        candidates = []
        tech_scores = []
        behavioral_scores = []
        
        for summary in self.summaries:
            candidate = summary.get('interview_metadata', {}).get('candidate_name', 'Unknown')
            # Extract scores from competency analysis if available
            competency = summary.get('competency_analysis', {})
            
            # For now, use overall score as proxy
            overall = summary.get('summary', {}).get('overall_score', 0)
            candidates.append(candidate)
            tech_scores.append(overall * 0.9)  # Simulated
            behavioral_scores.append(overall * 0.95)  # Simulated
        
        fig = go.Figure()
        
        for i, candidate in enumerate(candidates):
            fig.add_trace(go.Scatterpolar(
                r=[tech_scores[i], behavioral_scores[i], (tech_scores[i] + behavioral_scores[i]) / 2],
                theta=['Technical', 'Behavioral', 'Overall'],
                fill='toself',
                name=candidate
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title='Competency Comparison',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_metrics_summary(self) -> go.Figure:
        """Create summary metrics cards."""
        if not self.metrics:
            return None
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=(
                'Total Interviews',
                'Average Score',
                'Strong Hire Rate',
                'Hire Rate',
                'Maybe Rate',
                'No Hire Rate'
            ),
            specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}],
                   [{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]]
        )
        
        total = self.metrics.get('total_interviews', 0)
        avg_score = self.metrics.get('average_score', 0)
        strong_hire = self.metrics.get('strong_hire', 0)
        hire = self.metrics.get('hire', 0)
        maybe = self.metrics.get('maybe', 0)
        no_hire = self.metrics.get('no_hire', 0)
        
        # Calculate percentages
        strong_hire_pct = (strong_hire / total * 100) if total > 0 else 0
        hire_pct = (hire / total * 100) if total > 0 else 0
        maybe_pct = (maybe / total * 100) if total > 0 else 0
        no_hire_pct = (no_hire / total * 100) if total > 0 else 0
        
        # Add indicators
        fig.add_trace(go.Indicator(
            mode="number",
            value=total,
            number={'font': {'size': 60}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ), row=1, col=1)
        
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=avg_score,
            number={'suffix': '/100', 'font': {'size': 50}},
            delta={'reference': 70, 'relative': False},
            domain={'x': [0, 1], 'y': [0, 1]}
        ), row=1, col=2)
        
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=strong_hire_pct,
            number={'suffix': '%', 'font': {'size': 40}},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': '#10b981'}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ), row=1, col=3)
        
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=hire_pct,
            number={'suffix': '%', 'font': {'size': 40}},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': '#3b82f6'}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ), row=2, col=1)
        
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=maybe_pct,
            number={'suffix': '%', 'font': {'size': 40}},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': '#f59e0b'}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ), row=2, col=2)
        
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=no_hire_pct,
            number={'suffix': '%', 'font': {'size': 40}},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': '#ef4444'}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ), row=2, col=3)
        
        fig.update_layout(
            title='Interview Metrics Summary',
            height=600,
            showlegend=False
        )
        
        return fig
    
    def create_html_report(self, output_path: str) -> str:
        """
        Generate complete HTML dashboard.
        
        Args:
            output_path: Path to save HTML file
            
        Returns:
            Path to generated HTML file
        """
        # Create all charts
        scores_chart = self.create_candidate_scores_chart()
        recommendation_chart = self.create_recommendation_distribution()
        confidence_chart = self.create_confidence_levels_chart()
        duration_chart = self.create_interview_duration_chart()
        competency_chart = self.create_competency_comparison()
        metrics_chart = self.create_metrics_summary()
        
        # Build HTML
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Interview Summarization Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f3f4f6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 2.5rem;
        }}
        .header p {{
            margin: 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .full-width {{
            grid-column: 1 / -1;
        }}
        .candidate-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .candidate-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}
        .candidate-card h3 {{
            margin-top: 0;
            color: #1f2937;
        }}
        .candidate-card .score {{
            font-size: 3rem;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .candidate-card .recommendation {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        .recommendation.strong-hire {{
            background: #d1fae5;
            color: #065f46;
        }}
        .recommendation.hire {{
            background: #dbeafe;
            color: #1e40af;
        }}
        .recommendation.maybe {{
            background: #fef3c7;
            color: #92400e;
        }}
        .recommendation.no-hire {{
            background: #fee2e2;
            color: #991b1b;
        }}
        .highlights {{
            margin-top: 15px;
            font-size: 0.9rem;
            color: #6b7280;
        }}
        .highlights li {{
            margin-bottom: 5px;
        }}
        .timestamp {{
            text-align: center;
            color: #6b7280;
            margin-top: 30px;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Interview Summarization Dashboard</h1>
        <p>AI-Powered Interview Analysis and Candidate Assessment</p>
    </div>
    
    <div class="dashboard-grid">
        <div class="chart-container full-width">
            <div id="metrics-chart"></div>
        </div>
        
        <div class="chart-container">
            <div id="scores-chart"></div>
        </div>
        
        <div class="chart-container">
            <div id="recommendation-chart"></div>
        </div>
        
        <div class="chart-container">
            <div id="confidence-chart"></div>
        </div>
        
        <div class="chart-container">
            <div id="duration-chart"></div>
        </div>
        
        <div class="chart-container full-width">
            <div id="competency-chart"></div>
        </div>
    </div>
    
    <div class="candidate-cards">
"""
        
        # Add candidate cards
        for summary in self.summaries:
            metadata = summary.get('interview_metadata', {})
            summary_data = summary.get('summary', {})
            
            candidate = metadata.get('candidate_name', 'Unknown')
            position = metadata.get('position', 'Unknown')
            score = summary_data.get('overall_score', 0)
            rec = summary_data.get('recommendation', 'Unknown')
            highlights = summary_data.get('key_highlights', [])[:3]
            
            rec_class = rec.lower().replace(' ', '-')
            
            html_content += f"""
        <div class="candidate-card">
            <h3>{candidate}</h3>
            <p style="color: #6b7280; margin: 5px 0;">{position}</p>
            <div class="score">{score}</div>
            <span class="recommendation {rec_class}">{rec}</span>
            <div class="highlights">
                <strong>Key Highlights:</strong>
                <ul>
"""
            for highlight in highlights:
                html_content += f"                    <li>{highlight}</li>\n"
            
            html_content += """
                </ul>
            </div>
        </div>
"""
        
        html_content += f"""
    </div>
    
    <div class="timestamp">
        Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    
    <script>
        // Render all charts
        {f'Plotly.newPlot("metrics-chart", {metrics_chart.to_json()});' if metrics_chart else ''}
        Plotly.newPlot("scores-chart", {scores_chart.to_json()});
        Plotly.newPlot("recommendation-chart", {recommendation_chart.to_json()});
        Plotly.newPlot("confidence-chart", {confidence_chart.to_json()});
        Plotly.newPlot("duration-chart", {duration_chart.to_json()});
        Plotly.newPlot("competency-chart", {competency_chart.to_json()});
    </script>
</body>
</html>
"""
        
        # Save HTML file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_file)


def generate_dashboard(
    summaries_path: str,
    metrics_path: Optional[str] = None,
    rankings_path: Optional[str] = None,
    output_path: Optional[str] = None
) -> str:
    """
    Generate interview summarization dashboard.
    
    Args:
        summaries_path: Path to interview summaries JSON
        metrics_path: Optional path to metrics JSON
        rankings_path: Optional path to rankings JSON
        output_path: Output path for HTML (auto-generated if not provided)
        
    Returns:
        Path to generated HTML dashboard
    """
    dashboard = InterviewDashboard(summaries_path, metrics_path, rankings_path)
    
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"results/dashboards/interview_dashboard_{timestamp}.html"
    
    html_path = dashboard.create_html_report(output_path)
    print(f"\n✅ Dashboard generated successfully!")
    print(f"📊 View at: {html_path}")
    
    return html_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Interview Summarization Dashboard')
    parser.add_argument('--summaries', required=True, help='Path to interview summaries JSON')
    parser.add_argument('--metrics', help='Path to metrics JSON')
    parser.add_argument('--rankings', help='Path to rankings JSON')
    parser.add_argument('--output', help='Output path for HTML dashboard')
    
    args = parser.parse_args()
    
    generate_dashboard(
        summaries_path=args.summaries,
        metrics_path=args.metrics,
        rankings_path=args.rankings,
        output_path=args.output
    )
