"""
Static Results Report Generator

Generates a comprehensive HTML report for CV screening results.
Can be run standalone to create a detailed analysis report.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import base64


def load_results(results_path: str) -> List[Dict[str, Any]]:
    """Load screening results from JSON file."""
    with open(results_path, 'r') as f:
        return json.load(f)


def load_metrics(metrics_path: str) -> Dict[str, Any]:
    """Load metrics from JSON file."""
    with open(metrics_path, 'r') as f:
        return json.load(f)


def generate_html_report(results: List[Dict], metrics: Dict, output_path: str):
    """Generate comprehensive HTML report."""
    
    # Sort candidates by score
    sorted_results = sorted(
        results,
        key=lambda x: x.get('matching', {}).get('overall_score', 0),
        reverse=True
    )
    
    # Calculate additional statistics
    scores = [r.get('matching', {}).get('overall_score', 0) for r in results]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV Screening Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .header {{
            text-align: center;
            padding-bottom: 2rem;
            border-bottom: 3px solid #1f77b4;
            margin-bottom: 2rem;
        }}
        
        .header h1 {{
            color: #1f77b4;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.1rem;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }}
        
        .metric-card.green {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        
        .metric-card.blue {{
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        }}
        
        .metric-card.orange {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        .section {{
            margin: 3rem 0;
        }}
        
        .section-title {{
            font-size: 1.8rem;
            color: #1f77b4;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .candidate-card {{
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-left: 4px solid #1f77b4;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-radius: 4px;
            transition: transform 0.2s;
        }}
        
        .candidate-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .candidate-card.strong {{
            border-left-color: #28a745;
        }}
        
        .candidate-card.good {{
            border-left-color: #17a2b8;
        }}
        
        .candidate-card.possible {{
            border-left-color: #ffc107;
        }}
        
        .candidate-card.weak {{
            border-left-color: #dc3545;
        }}
        
        .candidate-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}
        
        .candidate-name {{
            font-size: 1.4rem;
            font-weight: 600;
            color: #333;
        }}
        
        .score-badge {{
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.2rem;
        }}
        
        .score-high {{
            background: #28a745;
            color: white;
        }}
        
        .score-medium {{
            background: #ffc107;
            color: #333;
        }}
        
        .score-low {{
            background: #dc3545;
            color: white;
        }}
        
        .candidate-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
            padding: 1rem;
            background: white;
            border-radius: 4px;
        }}
        
        .info-item {{
            text-align: center;
        }}
        
        .info-label {{
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 0.25rem;
        }}
        
        .info-value {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #1f77b4;
        }}
        
        .details-section {{
            margin-top: 1rem;
        }}
        
        .details-title {{
            font-weight: 600;
            color: #1f77b4;
            margin: 1rem 0 0.5rem 0;
        }}
        
        .list-item {{
            padding: 0.25rem 0;
            padding-left: 1.5rem;
            position: relative;
        }}
        
        .list-item:before {{
            content: "•";
            position: absolute;
            left: 0.5rem;
            color: #1f77b4;
        }}
        
        .recommendation-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-left: 1rem;
        }}
        
        .badge-strong {{
            background: #28a745;
            color: white;
        }}
        
        .badge-good {{
            background: #17a2b8;
            color: white;
        }}
        
        .badge-possible {{
            background: #ffc107;
            color: #333;
        }}
        
        .badge-weak {{
            background: #dc3545;
            color: white;
        }}
        
        .interview-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-left: 0.5rem;
        }}
        
        .interview-yes {{
            background: #28a745;
            color: white;
        }}
        
        .interview-no {{
            background: #dc3545;
            color: white;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 2px solid #e0e0e0;
            color: #666;
            font-size: 0.9rem;
        }}
        
        .print-button {{
            background: #1f77b4;
            color: white;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 4px;
            font-size: 1rem;
            cursor: pointer;
            margin: 1rem 0;
        }}
        
        .print-button:hover {{
            background: #155a8a;
        }}
        
        @media print {{
            body {{
                padding: 0;
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
            .print-button {{
                display: none;
            }}
            .candidate-card {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 CV Screening Results Report</h1>
            <p class="subtitle">Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
            <button class="print-button" onclick="window.print()">🖨️ Print Report</button>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{metrics.get('total_candidates', 0)}</div>
                <div class="metric-label">Total Candidates</div>
            </div>
            <div class="metric-card green">
                <div class="metric-value">{avg_score:.1f}</div>
                <div class="metric-label">Average Score</div>
            </div>
            <div class="metric-card blue">
                <div class="metric-value">{metrics.get('strong_matches', 0)}</div>
                <div class="metric-label">Strong Matches</div>
            </div>
            <div class="metric-card orange">
                <div class="metric-value">{metrics.get('interview_recommended', 0)}</div>
                <div class="metric-label">Interview Ready</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">Candidate Rankings</h2>
"""
    
    # Add each candidate
    for rank, result in enumerate(sorted_results, 1):
        matching = result.get('matching', {})
        qualifications = result.get('qualifications', {})
        
        name = result.get('candidate_name', 'Unknown')
        score = matching.get('overall_score', 0)
        recommendation = matching.get('recommendation', 'Unknown')
        interview = matching.get('interview_recommendation', False)
        
        # Determine card and badge classes
        rec_lower = recommendation.lower()
        if 'strong' in rec_lower:
            card_class = 'strong'
            badge_class = 'badge-strong'
        elif 'good' in rec_lower:
            card_class = 'good'
            badge_class = 'badge-good'
        elif 'possible' in rec_lower:
            card_class = 'possible'
            badge_class = 'badge-possible'
        else:
            card_class = 'weak'
            badge_class = 'badge-weak'
        
        score_class = 'score-high' if score >= 75 else 'score-medium' if score >= 50 else 'score-low'
        interview_badge_class = 'interview-yes' if interview else 'interview-no'
        interview_text = '✅ Interview' if interview else '❌ No Interview'
        
        html_content += f"""
            <div class="candidate-card {card_class}">
                <div class="candidate-header">
                    <div>
                        <span class="candidate-name">#{rank}. {name}</span>
                        <span class="recommendation-badge {badge_class}">{recommendation}</span>
                        <span class="interview-badge {interview_badge_class}">{interview_text}</span>
                    </div>
                    <span class="score-badge {score_class}">{score}/100</span>
                </div>
                
                <div class="candidate-info">
                    <div class="info-item">
                        <div class="info-label">Experience</div>
                        <div class="info-value">{qualifications.get('total_years_experience', 0)} years</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Education</div>
                        <div class="info-value">{qualifications.get('education_level', 'N/A')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Technical Skills</div>
                        <div class="info-value">{len(qualifications.get('technical_skills', []))}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Certifications</div>
                        <div class="info-value">{len(qualifications.get('relevant_certifications', []))}</div>
                    </div>
                </div>
                
                <div class="details-section">
                    <div class="details-title">💪 Strengths:</div>
"""
        
        strengths = matching.get('strengths', [])
        if strengths:
            for strength in strengths:
                html_content += f'                    <div class="list-item">{strength}</div>\n'
        else:
            html_content += '                    <div class="list-item">No strengths recorded</div>\n'
        
        html_content += """
                    <div class="details-title">⚠️ Gaps:</div>
"""
        
        gaps = matching.get('gaps', [])
        if gaps:
            for gap in gaps:
                html_content += f'                    <div class="list-item">{gap}</div>\n'
        else:
            html_content += '                    <div class="list-item">No gaps identified</div>\n'
        
        reasoning = matching.get('reasoning', 'No reasoning provided')
        html_content += f"""
                    <div class="details-title">💡 Reasoning:</div>
                    <div style="padding: 0.5rem; background: white; border-radius: 4px; margin-top: 0.5rem;">
                        {reasoning}
                    </div>
                </div>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="footer">
            <p><strong>HR AI Lab</strong> - Powered by Google Gemini 2.5 Flash-Lite</p>
            <p>CV Screening Dashboard • {datetime.now().year}</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Write to file
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    print(f"✅ HTML report generated: {output_path}")


def main():
    """Generate report for latest results."""
    results_dir = Path("results/cv_screening")
    
    # Find latest results
    result_files = sorted(results_dir.glob("screening_results_*.json"), reverse=True)
    
    if not result_files:
        print("❌ No screening results found")
        return
    
    latest_result = result_files[0]
    metrics_file = latest_result.parent / latest_result.name.replace("screening_results_", "screening_metrics_")
    
    print(f"📊 Generating report from: {latest_result.name}")
    
    # Load data
    results = load_results(str(latest_result))
    metrics = load_metrics(str(metrics_file)) if metrics_file.exists() else {}
    
    # Generate report
    output_path = results_dir.parent / "dashboards" / f"cv_screening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    generate_html_report(results, metrics, str(output_path))
    
    print(f"🌐 Open the report in your browser: {output_path}")


if __name__ == "__main__":
    main()
