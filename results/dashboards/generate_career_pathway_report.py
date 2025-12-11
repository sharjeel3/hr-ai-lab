"""
Generate HTML Report for Career Pathway Recommendations

Creates a comprehensive, static HTML report with visualizations
that can be shared without requiring a running Streamlit server.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np


def load_latest_results(results_dir: Path) -> Dict[str, Any]:
    """Load the most recent recommendation results."""
    files = list(results_dir.glob('recommendations_*.json'))
    
    if not files:
        raise FileNotFoundError("No recommendation results found")
    
    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    
    with open(latest_file, 'r') as f:
        return json.load(f)


def create_overview_section(data: Dict[str, Any]) -> str:
    """Create HTML for overview section."""
    metrics = data.get('metrics', {})
    recommendations = data.get('recommendations', [])
    
    total_employees = metrics.get('total_employees', len(recommendations))
    success_rate = metrics.get('success_rate', 0) * 100
    avg_score = metrics.get('average_similarity_score', 0) * 100
    unique_roles = metrics.get('unique_roles_recommended', 0)
    
    html = f"""
    <div class="overview-section">
        <h2>📊 Overview</h2>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{total_employees}</div>
                <div class="metric-label">Total Employees</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{success_rate:.1f}%</div>
                <div class="metric-label">Success Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{avg_score:.1f}%</div>
                <div class="metric-label">Avg Match Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{unique_roles}</div>
                <div class="metric-label">Unique Roles</div>
            </div>
        </div>
    </div>
    """
    
    return html


def create_similarity_distribution_chart(recommendations: List[Dict]) -> str:
    """Create similarity score distribution chart."""
    scores = []
    for rec in recommendations:
        for item in rec.get('recommendations', []):
            scores.append(item['similarity_score'] * 100)
    
    if not scores:
        return ""
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=scores,
        nbinsx=20,
        marker_color='rgba(102, 126, 234, 0.7)',
        name='Distribution'
    ))
    
    mean_score = np.mean(scores)
    fig.add_vline(
        x=mean_score,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean_score:.1f}%"
    )
    
    fig.update_layout(
        title="Match Score Distribution",
        xaxis_title="Match Score (%)",
        yaxis_title="Frequency",
        height=400,
        showlegend=False
    )
    
    return fig.to_html(include_plotlyjs='cdn', div_id='similarity_dist')


def create_role_popularity_chart(recommendations: List[Dict]) -> str:
    """Create chart of most recommended roles."""
    role_counts = {}
    
    for rec in recommendations:
        for item in rec.get('recommendations', []):
            role_title = item['role']['title']
            role_counts[role_title] = role_counts.get(role_title, 0) + 1
    
    if not role_counts:
        return ""
    
    sorted_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    roles, counts = zip(*sorted_roles)
    
    fig = go.Figure(go.Bar(
        y=roles,
        x=counts,
        orientation='h',
        marker_color='rgba(118, 75, 162, 0.7)'
    ))
    
    fig.update_layout(
        title="Top 10 Most Recommended Roles",
        xaxis_title="Number of Recommendations",
        yaxis_title="Role Title",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig.to_html(include_plotlyjs=False, div_id='role_popularity')


def create_job_family_chart(recommendations: List[Dict]) -> str:
    """Create job family breakdown pie chart."""
    family_counts = {}
    
    for rec in recommendations:
        for item in rec.get('recommendations', []):
            family = item['role']['job_family']
            family_counts[family] = family_counts.get(family, 0) + 1
    
    if not family_counts:
        return ""
    
    fig = go.Figure(go.Pie(
        labels=list(family_counts.keys()),
        values=list(family_counts.values()),
        hole=0.4,
        marker_colors=px.colors.qualitative.Set3
    ))
    
    fig.update_layout(
        title="Recommendations by Job Family",
        height=400
    )
    
    return fig.to_html(include_plotlyjs=False, div_id='job_family')


def create_employee_section(employee_data: Dict[str, Any]) -> str:
    """Create HTML for a single employee's recommendations."""
    html = f"""
    <div class="employee-section">
        <h3>👤 {employee_data['employee_name']}</h3>
        <p><strong>Employee ID:</strong> {employee_data['employee_id']}</p>
        <p><strong>Current Title:</strong> {employee_data['current_title']}</p>
        <p><strong>Recommendations:</strong> {len(employee_data.get('recommendations', []))}</p>
    """
    
    for idx, rec in enumerate(employee_data.get('recommendations', []), 1):
        role = rec['role']
        score = rec['similarity_score'] * 100
        
        score_class = 'excellent' if score >= 80 else 'good' if score >= 70 else 'fair'
        
        html += f"""
        <div class="recommendation-card">
            <h4>{idx}. {role['title']} - {role['job_family']}</h4>
            <div class="recommendation-details">
                <div class="detail-row">
                    <span class="label">Match Score:</span>
                    <span class="value score-{score_class}">{score:.1f}%</span>
                </div>
                <div class="detail-row">
                    <span class="label">Experience Required:</span>
                    <span class="value">{role['years_experience']} years</span>
                </div>
                <div class="detail-row">
                    <span class="label">Salary Range:</span>
                    <span class="value">{role['salary_range']}</span>
                </div>
            </div>
            
            <div class="section">
                <strong>Key Responsibilities:</strong>
                <ul>
        """
        
        for resp in role['responsibilities'][:3]:
            html += f"<li>{resp}</li>"
        
        html += """
                </ul>
            </div>
            
            <div class="section">
                <strong>Required Skills:</strong>
                <div class="skills-container">
        """
        
        for skill in role['required_skills'][:6]:
            html += f'<span class="skill-badge">{skill}</span>'
        
        html += f"""
                </div>
            </div>
            
            <div class="section">
                <strong>💡 Why This Role?</strong>
                <p class="explanation">{rec['explanation'][:400]}...</p>
            </div>
            
            <div class="development-plan">
                <strong>📈 90-Day Development Plan</strong>
        """
        
        plan = rec.get('development_plan', {})
        for month_key in ['month_1', 'month_2', 'month_3']:
            if month_key in plan:
                month_num = month_key.split('_')[1]
                month_data = plan[month_key]
                
                html += f"""
                <div class="month-section">
                    <strong>Month {month_num}: {month_data.get('focus', 'N/A')}</strong>
                    <ul class="objectives">
                """
                
                for obj in month_data.get('objectives', [])[:2]:
                    html += f"<li>{obj}</li>"
                
                html += """
                    </ul>
                </div>
                """
        
        if 'total_estimated_hours' in plan:
            html += f"<p><em>Total Estimated Hours: {plan['total_estimated_hours']}</em></p>"
        
        html += """
            </div>
        </div>
        """
    
    html += "</div>"
    return html


def generate_html_report(data: Dict[str, Any], output_path: Path) -> None:
    """Generate complete HTML report."""
    
    recommendations = data.get('recommendations', [])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create visualizations
    similarity_chart = create_similarity_distribution_chart(recommendations)
    role_chart = create_role_popularity_chart(recommendations)
    family_chart = create_job_family_chart(recommendations)
    
    # Build employee sections
    employee_sections = []
    for emp in recommendations[:10]:  # Limit to first 10 for report size
        employee_sections.append(create_employee_section(emp))
    
    # HTML template
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Career Pathway Recommendations Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 1rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 2rem;
        }}
        
        .overview-section {{
            margin-bottom: 3rem;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 0.75rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .metric-label {{
            font-size: 1rem;
            opacity: 0.9;
        }}
        
        .charts-section {{
            margin: 3rem 0;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 2rem;
            margin-top: 1.5rem;
        }}
        
        .chart-container {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 0.75rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .employee-section {{
            margin: 2rem 0;
            padding: 2rem;
            background: #f8f9fa;
            border-radius: 0.75rem;
            border-left: 4px solid #667eea;
        }}
        
        .employee-section h3 {{
            color: #667eea;
            margin-bottom: 1rem;
        }}
        
        .recommendation-card {{
            background: white;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0.5rem;
            border-left: 3px solid #28a745;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }}
        
        .recommendation-card h4 {{
            color: #333;
            margin-bottom: 1rem;
        }}
        
        .recommendation-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 0.5rem;
        }}
        
        .detail-row {{
            display: flex;
            flex-direction: column;
        }}
        
        .detail-row .label {{
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 0.25rem;
        }}
        
        .detail-row .value {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
        }}
        
        .score-excellent {{
            color: #28a745;
        }}
        
        .score-good {{
            color: #17a2b8;
        }}
        
        .score-fair {{
            color: #ffc107;
        }}
        
        .section {{
            margin: 1.5rem 0;
        }}
        
        .section strong {{
            color: #667eea;
            display: block;
            margin-bottom: 0.5rem;
        }}
        
        .section ul {{
            list-style-position: inside;
            margin-left: 1rem;
        }}
        
        .section li {{
            margin: 0.5rem 0;
        }}
        
        .skills-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }}
        
        .skill-badge {{
            background: #667eea;
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 1rem;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .explanation {{
            background: #e7f3ff;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 3px solid #17a2b8;
            margin-top: 0.5rem;
        }}
        
        .development-plan {{
            background: #f0f8ff;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-top: 1.5rem;
        }}
        
        .month-section {{
            margin: 1rem 0;
            padding-left: 1rem;
            border-left: 2px solid #667eea;
        }}
        
        .objectives {{
            list-style-position: inside;
            margin: 0.5rem 0;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 2rem;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        
        h2 {{
            color: #667eea;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Career Pathway Recommendations Report</h1>
            <p>Generated on {timestamp}</p>
        </div>
        
        <div class="content">
            {create_overview_section(data)}
            
            <div class="charts-section">
                <h2>📊 Visualizations</h2>
                <div class="charts-grid">
                    <div class="chart-container">
                        {similarity_chart}
                    </div>
                    <div class="chart-container">
                        {role_chart}
                    </div>
                </div>
                <div style="margin-top: 2rem;">
                    <div class="chart-container">
                        {family_chart}
                    </div>
                </div>
            </div>
            
            <h2>👥 Employee Recommendations</h2>
            {''.join(employee_sections)}
        </div>
        
        <div class="footer">
            <p><strong>Career Pathway Recommender Dashboard</strong></p>
            <p>HR AI Lab | Powered by Google Gemini 2.5 Flash-Lite & sentence-transformers</p>
        </div>
    </div>
</body>
</html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Report generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate Career Pathway HTML Report')
    parser.add_argument(
        '--input',
        type=str,
        help='Path to recommendations JSON file (default: latest in results/career_pathway)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output HTML file path (default: results/dashboards/career_pathway_report_TIMESTAMP.html)'
    )
    
    args = parser.parse_args()
    
    # Determine paths
    if args.input:
        input_path = Path(args.input)
        with open(input_path, 'r') as f:
            data = json.load(f)
    else:
        results_dir = Path(__file__).parent.parent / 'career_pathway'
        data = load_latest_results(results_dir)
    
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = Path(__file__).parent / f'career_pathway_report_{timestamp}.html'
    
    # Generate report
    generate_html_report(data, output_path)
    
    print(f"\n🌐 Open in browser: file://{output_path.absolute()}")


if __name__ == '__main__':
    main()
